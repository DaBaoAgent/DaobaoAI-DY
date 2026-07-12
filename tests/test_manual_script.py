from __future__ import annotations

import unittest
import tempfile
import json
from pathlib import Path

from backend.manual_script import (
    ScriptBlock,
    SubtitleLine,
    _clean_for_match,
    match_source_block,
    parse_srt_file,
)
from anchored_pipeline import _reserve_source_clip, _source_dialogue_slices, load_script_table_source_clips
from backend.visual_matcher import VisualIntervalAllocator


def subtitle(index: int, start: float, end: float, text: str) -> SubtitleLine:
    return SubtitleLine(index, start, end, text, _clean_for_match(text))


class MatchSourceBlockTests(unittest.TestCase):
    def test_parses_ass_dialogue_lines_for_manual_matching(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "episode.ass"
            path.write_text(
                "[Script Info]\nTitle: test\n\n"
                "[Events]\n"
                "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
                "Dialogue: 0,0:01:02.20,0:01:04.50,Default,,0,0,0,,{\\an8}第一句\\N第二句\n",
                "utf-8",
            )

            lines = parse_srt_file(path)

            self.assertEqual(len(lines), 1)
            self.assertAlmostEqual(lines[0].start, 62.2)
            self.assertAlmostEqual(lines[0].end, 64.5)
            self.assertEqual(lines[0].text, "第一句 第二句")

    def test_keeps_separated_requested_lines_as_separate_intervals(self) -> None:
        subtitles = [
            subtitle(1, 10.0, 11.0, "第一句"),
            subtitle(2, 11.2, 14.0, "没有指定的长对白"),
            subtitle(3, 20.0, 21.0, "第二句"),
            subtitle(4, 21.2, 25.0, "另一段没有指定的对白"),
            subtitle(5, 30.0, 31.0, "第三句"),
        ]
        block = ScriptBlock("source_clip", "第一句\n第二句\n第三句", "")

        result = match_source_block(block, subtitles)

        self.assertEqual(result["match_mode"], "exact_script_lines")
        self.assertEqual(
            [(part["start"], part["end"]) for part in result["intervals"]],
            [(10.0, 11.0), (20.0, 21.0), (30.0, 31.0)],
        )

    def test_keeps_adjacent_requested_subtitles_as_separate_intervals(self) -> None:
        subtitles = [
            subtitle(1, 10.0, 11.0, "第一句"),
            subtitle(2, 11.3, 12.0, "第二句"),
            subtitle(3, 12.1, 13.0, "未指定对白"),
            subtitle(4, 14.0, 15.0, "第三句"),
        ]
        block = ScriptBlock("source_clip", "第一句\n第二句\n第三句", "")

        result = match_source_block(block, subtitles)

        self.assertEqual(
            [(part["start"], part["end"]) for part in result["intervals"]],
            [(10.0, 11.0), (11.3, 12.0), (14.0, 15.0)],
        )

    def test_source_dialogue_slices_drop_overlapping_duplicate_subtitles(self) -> None:
        records = [
            {"source_index": 1, "start": 1680.733, "end": 1685.733, "text": "第一句"},
            {"source_index": 1, "start": 1684.4, "end": 1685.733, "text": "重复字幕"},
            {"source_index": 1, "start": 1686.6, "end": 1687.6, "text": "第二句"},
        ]

        slices = _source_dialogue_slices(records, 1680.733, 1687.6, 1)

        self.assertEqual(
            [(start, end) for start, end, _ in slices],
            [(1680.733, 1685.733), (1686.6, 1687.6)],
        )

    def test_adjacent_source_clips_can_be_reserved_without_guard_gap(self) -> None:
        allocator = VisualIntervalAllocator(20.0, [], guard=0.18)

        _reserve_source_clip(allocator, 10.0, 11.0, "原片行1")
        _reserve_source_clip(allocator, 11.0, 12.0, "原片行2")

        self.assertEqual(len(allocator.used), 2)

    def test_load_script_table_source_clips_skips_duplicate_source_ranges(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            table = {
                "script_source": "manual_upload",
                "rows": [
                    {"row_id": 1, "row_type": "source_clip", "source_start": 10.0, "source_end": 11.0,
                     "source_index": 1, "text": "原片对白：第一句", "use_exact_duration": True},
                    {"row_id": 2, "row_type": "source_clip", "source_start": 11.0, "source_end": 12.0,
                     "source_index": 1, "text": "原片对白：第二句", "use_exact_duration": True},
                    {"row_id": 3, "row_type": "source_clip", "source_start": 11.0, "source_end": 12.0,
                     "source_index": 1, "text": "原片对白：第二句重复", "use_exact_duration": True},
                ],
            }
            subtitles = {
                "subtitles": [
                    {"source_index": 1, "start": 10.0, "end": 11.0, "text": "第一句"},
                    {"source_index": 1, "start": 11.0, "end": 12.0, "text": "第二句"},
                ],
            }
            (folder / "_drama_script_table.json").write_text(json.dumps(table, ensure_ascii=False), "utf-8")
            (folder / "_source_subtitle_index.json").write_text(json.dumps(subtitles, ensure_ascii=False), "utf-8")

            clips = load_script_table_source_clips(folder, 0.0, 20.0, 20.0)

            self.assertEqual([(clip.clip_start, clip.clip_end) for clip in clips], [(10.0, 11.0), (11.0, 12.0)])


if __name__ == "__main__":
    unittest.main()
