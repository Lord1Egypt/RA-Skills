---
name: tianpuyue_music
description: 使用天谱乐 AI 生成纯音乐、歌曲（含人声演唱）或歌词，将结果保存到本地。当用户提到"天谱乐""天璞悦""Tianpuyue""Tempolor""AI 作曲""AI 音乐""生成音乐""生成歌曲""生成歌词""BGM""背景音乐"时引用；当用户需要为视频、游戏或内容创作配乐时引用；当用户需要纯音乐（无人声）时引用；当用户需要带人声演唱的完整歌曲时引用；当用户需要 AI 写歌词时引用。当用户同时提到"工作流""流水线""编排"时，不应直接引用此 skill，应优先让 content_generation_workflow 统一调度。
metadata:
  openclaw:
    requires:
      bins:
        - uv
      anyBins:
        - python
        - python3
        - py
      env:
        - TIANPUYUE_API_KEY
        - OUTPUT_ROOT
    primaryEnv: TIANPUYUE_API_KEY
---

# 天谱乐音乐生成

这个 skill 是纯内容生成能力，负责天谱乐的纯音乐/歌曲/歌词任务创建、状态查询和本地下载，不负责对象存储上传或分享链接生成。

适用场景：

- 用户明确指定使用天谱乐生成纯音乐、歌曲或歌词
- 多媒体工作流需要一个音乐生成供应商
- 已有 `item_id`，只需要查询进度或下载本地结果

## 使用脚本

脚本位于 skill 目录内的 `scripts/`，运行时始终使用绝对路径。

设 `TP_SKILL_DIR` 为 `.claude/skills/tianpuyue_music` 的绝对路径：

- 纯音乐生成（完整流程）：`uv run --python python $TP_SKILL_DIR/scripts/generate_music.py --prompt "..." --name "忧伤钢琴曲"`
- 歌曲生成（完整流程）：`uv run --python python $TP_SKILL_DIR/scripts/generate_song.py --prompt "..." --name "夏日海边"`
- 歌词生成（完整流程）：`uv run --python python $TP_SKILL_DIR/scripts/generate_lyrics.py --prompt "..." --name "青春离别"`
- 纯音乐状态查询：`uv run --python python $TP_SKILL_DIR/scripts/query_music_status.py --item-id <ID>`
- 歌曲状态查询：`uv run --python python $TP_SKILL_DIR/scripts/query_song_status.py --item-id <ID>`
- 歌词状态查询：`uv run --python python $TP_SKILL_DIR/scripts/query_lyrics_status.py --item-id <ID>`

## 脚本参数

### 纯音乐生成

| 参数 | 必需 | 说明 |
|------|------|------|
| `--prompt` | 是 | 音乐描述提示词，可包含节奏、调性、和弦、时长等 |
| `--name` | 否 | 文件名描述，不超过 10 个中文字 |
| `--model` | 否 | 模型名称，默认 `TemPolor i3.5` |
| `--poll-interval` | 否 | 轮询间隔秒数，默认 15 |
| `--timeout` | 否 | 超时秒数，默认 900 |

### 歌曲生成

| 参数 | 必需 | 说明 |
|------|------|------|
| `--prompt` | 是 | 音乐描述提示词 |
| `--name` | 否 | 文件名描述，不超过 10 个中文字 |
| `--model` | 否 | 模型名称，默认 `TemPolor v4.5` |
| `--lyrics` | 否 | 自定义歌词（为空时自动生成） |
| `--voice-id` | 否 | 演唱声音 ID，参考 `references/voice_id_map.md` |
| `--poll-interval` | 否 | 轮询间隔秒数，默认 15 |
| `--timeout` | 否 | 超时秒数，默认 900 |

### 歌词生成

| 参数 | 必需 | 说明 |
|------|------|------|
| `--prompt` | 是 | 歌词生成的提示文本 |
| `--name` | 否 | 文件名描述，不超过 10 个中文字 |
| `--song-model` | 否 | 适配的歌曲模型名称，默认 `TemPolor v4.5` |
| `--poll-interval` | 否 | 轮询间隔秒数，默认 10 |
| `--timeout` | 否 | 超时秒数，默认 300 |

## 输出约定

- 本地输出目录（相对于 `OUTPUT_ROOT`，默认为项目根目录）：
  - `outputs/tianpuyue/music/`
  - `outputs/tianpuyue/songs/`
  - `outputs/tianpuyue/lyrics/`
- 纯音乐/歌曲输出 JSON 至少包含：
  - `type` — `music` / `song`
  - `provider` — `tianpuyue`
  - `item_id`
  - `local_path`
  - `source_url`
- 歌词输出 JSON 至少包含：
  - `type` — `lyrics`
  - `provider` — `tianpuyue`
  - `item_id`
  - `local_path`
  - `title`
  - `lyric`

## 配置

- 环境变量：`TIANPUYUE_API_KEY`（必需，未设置时直接报错）
- 环境变量：`TIANPUYUE_CALLBACK_URL`（可选，轮询模式下使用占位值即可）
- 环境变量：`OUTPUT_ROOT`（可选，输出根目录，支持 `~` 展开，默认为用户主目录）

## 协作方式

- 如果用户只要求生成并得到本地文件，本 skill 可直接完成
- 如果用户还需要可访问链接，应由后续的交付环节继续处理
- 当用户未指定供应商时，是否使用天谱乐由多媒体内容生成 Agent 的预设策略决定
