# DaobaoAI-DY | 大宝短剧/电视剧智能剪辑工厂

**中文简介**  
DaobaoAI-DY 是一套面向短剧、电视剧解说、影视二创和短视频生产的 AI 智能剪辑工具。它将原片、SRT/ASS 字幕和人工解说文案组合起来，通过视觉识别、字幕定位、广告过滤、AI 配音和自动成片流程，帮助创作者更快完成剧情解说、批量混剪、口播剪辑和短视频发布素材生产。

**English Summary**  
DaobaoAI-DY is an AI-powered video editing workflow for short drama clips, TV-series commentary, drama recap automation, and short-video production. It combines source videos, subtitles, and manual narration scripts with visual analysis, subtitle alignment, ad filtering, AI voice generation, and automated rendering to help creators produce story-driven clips faster.

## GitHub Search Keywords | GitHub 搜索关键词

`AI video editor`, `short drama video editing`, `drama recap automation`, `TV series commentary`, `AI narration`, `subtitle alignment`, `automatic video editing`, `FastAPI`, `React`, `Vite`, `DashScope`, `Qwen TTS`, `GPT-SoVITS`, `短剧剪辑`, `电视剧解说`, `影视二创`, `自动剪辑`, `AI配音`, `字幕定位`, `广告过滤`, `短视频成片`

Suggested repository topics:

```text
ai-video-editor
short-video
drama-recap
video-automation
subtitle-alignment
ai-narration
fastapi
react
vite
dashscope
qwen-tts
gpt-sovits
```

Suggested GitHub description:

```text
DaobaoAI-DY | 大宝短剧/电视剧智能剪辑工厂: AI video editor for drama recaps, TV commentary, subtitle alignment, AI narration, ad filtering, and automated short-video rendering.
```

## Features | 核心功能

- **Material detection | 素材检测**: detect source videos, subtitle files, and commentary scripts before rendering.
- **Subtitle alignment | 字幕定位**: align manual source-dialogue blocks with SRT/ASS subtitle timestamps.
- **Visual indexing | 视觉索引**: call visual models to identify characters, scenes, actions, and usable frames.
- **Ad filtering | 广告过滤**: merge subtitle and visual ad signals to avoid commercial segments.
- **AI voice workflow | AI 配音流程**: support DashScope/Qwen voice synthesis and optional local GPT-SoVITS workflows.
- **Automated rendering | 自动成片**: combine source clips, narration audio, subtitles, and matched visuals into final videos.
- **Web UI | 网页界面**: FastAPI backend with a React/Vite frontend for creator-friendly operation.

## Tech Stack | 技术栈

- Backend: Python, FastAPI, Pydantic, Uvicorn
- Frontend: React, TypeScript, Vite, Lucide React
- AI services: Alibaba Cloud DashScope / Qwen TTS, optional GPT-SoVITS
- Media tooling: FFmpeg / FFprobe

## Project Structure | 项目结构

```text
DaobaoAI-DY/
  app.py
  launch_dabaoai.py
  anchored_pipeline.py
  backend/
  frontend/
  tests/
  requirements.txt
```

## Clone | 克隆项目

```bash
git clone https://github.com/DaBaoAgent/DaobaoAI-DY.git
cd DaobaoAI-DY
```

## Install | 安装

### Backend | 后端

Python 3.11+ is recommended.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Frontend | 前端

```bash
cd frontend
npm install
npm run build
cd ..
```

### FFmpeg | 媒体工具

Install FFmpeg and make sure `ffmpeg` and `ffprobe` are available in your system PATH, or place them under:

```text
tools/ffmpeg/bin/
```

## Configure | 配置

DaobaoAI-DY can read API keys from environment variables:

```bash
DASHSCOPE_API_KEY=your_dashscope_key
SILICONFLOW_API_KEY=your_siliconflow_key
```

You can also configure API keys in the Web UI after startup.

Local files such as `.env`, `config/secrets.bin`, `config/.secret.key`, `config/user_config.json`, `runtime/`, generated videos, generated audio, and private voice clone profiles should not be committed.

## Run | 启动

```bash
python launch_dabaoai.py
```

Open:

```text
http://127.0.0.1:7861/
```

Direct backend startup:

```bash
python -m uvicorn app:app --host 127.0.0.1 --port 7861
```

## Usage Workflow | 使用流程

1. Open the Web UI and configure API keys or voice settings.  
   打开 Web UI，配置 API Key 或配音参数。
2. Upload or select source video, SRT/ASS subtitles, and a commentary script.  
   上传或选择原片、字幕文件和解说文案。
3. Run visual recognition to build a source visual index.  
   运行视觉识别，生成原片视觉索引。
4. Generate the script table to align source-dialogue blocks and narration blocks.  
   生成脚本表，完成原片台词段和解说段定位。
5. Test AI voice output, then start automated rendering.  
   测试 AI 配音，确认后开始自动成片。
6. Review generated videos, subtitles, and matching reports in the output folder.  
   在输出目录检查成片、字幕和匹配报告。

## Script Format | 文案格式

Use clear source/narration blocks:

```text
原片：
角色对白或需要保留的原片台词

解说：
这里填写解说文案
```

## Tests | 测试

```bash
python -m unittest discover tests
```

## Security Notes | 安全说明

- Do not commit API keys, local user configuration, runtime files, videos, audio, subtitles, or private voice clone profiles.
- 不要提交 API Key、本机配置、运行缓存、视频音频素材、字幕文件或私有克隆音色配置。
- Review `.gitignore` before publishing a public repository.
- 发布公开仓库前请复查 `.gitignore` 和待提交文件。

## Contributor | 贡献者

- Dabao

## License | 许可证

No license has been declared yet. Add a license before public collaboration or commercial distribution.
