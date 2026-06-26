# videototext — 参考

## 技能包内源码镜像（与仓库同路径）

以下文件在 **`code/app/...`** 下各有一份，与主仓库 `app/...` 对应；主仓库更新后请自行同步复制。

| 主题 | 包内路径 |
|------|----------|
| B 站抽取（yt-dlp + 字幕服务） | `code/app/extractors/bilibili.py` |
| 抽取基类 / ParseContext | `code/app/extractors/base.py` |
| 字幕 HTTP、Cookie、view/player、节流重试 | `code/app/services/bilibili_subtitle.py` |
| 总结 LLM + 回退 | `code/app/services/summary.py` |
| 配置项定义（技能包内已适配 `.env` 根目录） | `code/app/core/settings.py` |
| 错误码 | `code/app/core/errors.py` |
| 时长覆盖、标题匹配分 | `code/app/utils/bilibili_subtitle_validate.py` |
| URL / 平台 | `code/app/utils/url_tools.py` |

运行依赖见 **`requirements-code.txt`**；环境变量模板见 **主仓库** 根目录 **`.env.example`**（技能包内不再附带副本）。

## 完整仓库中的其它路径（未打入技能包 code/）

| 主题 | 路径 |
|------|------|
| 编排（字幕 → ASR → 总结） | `app/services/orchestrator.py` |
| 本机 ASR | `app/asr/local_faster_whisper.py`、`app/utils/audio_fetch.py` |

## 环境变量速查

以下名称与 `.env.example` / `Settings` 一致；具体默认值以 `app/core/settings.py` 为准。

### B 站请求与字幕质量

- `BILIBILI_MIN_INTERVAL_SECONDS` — 请求最小间隔（秒）
- `BILIBILI_MAX_RETRIES`、`BILIBILI_BACKOFF_BASE_SECONDS` — 重试与退避
- `BILIBILI_SUBTITLE_VALIDATE` — 是否启用时长/标题校验与多轮择优
- `BILIBILI_SUBTITLE_SAMPLE_ROUNDS`、`BILIBILI_SUBTITLE_SAMPLE_ROUND_SLEEP_SECONDS`
- `BILIBILI_PLAYER_SUBTITLE_EMPTY_RETRIES`、`BILIBILI_PLAYER_SUBTITLE_EMPTY_RETRY_SLEEP_SECONDS`
- `BILIBILI_SUBTITLE_MIN_COVERAGE_RATIO`、`BILIBILI_SUBTITLE_MIN_DURATION_FOR_COVERAGE_CHECK_SECONDS`
- `BILIBILI_SUBTITLE_LONG_VIDEO_MIN_DURATION_SECONDS`、`BILIBILI_SUBTITLE_LONG_VIDEO_MIN_BODY_LINES`
- `BILIBILI_SUBTITLE_MIN_TITLE_MATCH_SCORE`、`BILIBILI_SUBTITLE_RELAXED_TITLE_MATCH_SCORE`
- `BILIBILI_SUBTITLE_MIN_TITLE_CHARS_FOR_MATCH`
- `BILIBILI_SUBTITLE_AI_MIN_TITLE_MATCH`、`BILIBILI_SUBTITLE_AI_SANITY_WHEN_VALIDATE_OFF`

### B 站 Cookie

- `SESSDATA`（或 `BILIBILI_SESSION_TOKEN`）
- `BILI_JCT`、`DEDEUSERID`、`DEDEUSERID__CKMD5`

### 本机 ASR（可选）

- `LOCAL_ASR_ENABLED`、`LOCAL_ASR_WHEN_SUBTITLE_FAILS`
- `LOCAL_ASR_MODEL`、`LOCAL_ASR_DEVICE`、`LOCAL_ASR_SPEED_PROFILE` 等（见 `.env.example`）

### 总结（OpenAI 兼容）

- `SUMMARY_ENABLED`
- `SUMMARY_LLM_BASE_URL`（别名含 `OPENAI_BASE_URL`）
- `SUMMARY_LLM_CHAT_COMPLETIONS_URL`（别名含 `OPENAI_CHAT_COMPLETIONS_URL`）
- `SUMMARY_LLM_API_KEY`（别名含 `OPENAI_API_KEY`）
- `SUMMARY_LLM_MODEL`（别名含 `OPENAI_MODEL`）
- `SUMMARY_LLM_TIMEOUT_SECONDS`、`SUMMARY_LLM_TEMPERATURE`

## 金丝雀脚本

```bash
python scripts/verify_subtitle_canary.py
# 仅校验不写摘要目录：
python scripts/verify_subtitle_canary.py --no-write
```

依赖与说明见仓库根目录 `CLAUDE.md`。
