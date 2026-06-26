---
name: videototext
description: >-
  指导稳定拉取 B 站官方字幕（应对限流/登录可见轨道）、并用 OpenAI 兼容接口生成中文总结稿；技能包内含 code/ 镜像源码与 env 模板，可打 zip 给 OpenClaw 离线使用。
  适用于 Bilibili 链接解析、字幕提取失败排查、SESSDATA/Cookie、WBI player 字幕、字幕校验与多轮采样、以及 SUMMARY_LLM_* 总结配置。
---

# videototext（B 站字幕 + 总结）

## 合规与前提

- 仅使用**用户本人账号**导出的 Cookie；不协助绕过付费墙、地域限制或批量爬取。
- 尊重站点频率限制：项目内已对 B 站 HTTP 做**节流 + 重试退避**，修改时不要去掉 `_throttle` / `_request_with_retry` 逻辑。
- 详细环境变量与默认值见同目录 [reference.md](reference.md)。
- **技能包内**已附带与主流程一致的源码镜像：见 [code/](code/)（导入方式见 [code/README.md](code/README.md)）。环境变量名与示例见 **主仓库** 根目录 `.env.example`，自行复制为技能包根目录的 `.env` 后填写。

## 端到端流程（与代码一致）

1. **URL**：`app/utils/url_tools.py`（包内 [code/app/utils/url_tools.py](code/app/utils/url_tools.py)）— 展开 `b23.tv`、解析 `BV` 与分 P `?p=`。
2. **编排**（完整仓库）：`app/services/orchestrator.py` — 先官方字幕；失败且开启 ASR 时再本机转写；正文就绪后调用总结服务。**技能包未含 orchestrator/ASR**，仅含抽取与总结核心模块。
3. **B 站元数据与字幕**：`app/extractors/bilibili.py` + `app/services/bilibili_subtitle.py`（包内 `code/app/...`）。
4. **无字幕兜底**（仅完整仓库）：`app/utils/audio_fetch.py` + `app/asr/local_faster_whisper.py`（需 `LOCAL_ASR_ENABLED` 等）。
5. **总结**：`app/services/summary.py` — 优先 LLM（OpenAI 兼容 Chat Completions），失败则本地抽样回退。

## 字幕链路：反爬与稳定性要点

### Cookie 策略（核心）

- `SESSDATA`（及可选 `BILI_JCT`、`DEDEUSERID`、`DEDEUSERID__CKMD5`）由 `app/services/bilibili_subtitle.py` 中 `_build_bilibili_cookie()` 组装为 `Cookie` 请求头。
- **优先带 Cookie 请求**；若仍失败再尝试无 Cookie（同一套 view → player 流程）。
- **需登录才返回的字幕**（`need_login_subtitle`）：仅 SESSDATA 往往不够，应配齐四件套（见 `.env.example` 注释）。
- **yt-dlp** 取信息与音频时复用同一 Cookie：`get_bilibili_sessdata_cookie_header()`（`app/extractors/bilibili.py`）。

### HTTP 行为

- 统一 **Referer** `https://www.bilibili.com/`、桌面 Chrome **User-Agent**、Accept JSON（`_client_headers`）。
- **全站最小请求间隔** `BILIBILI_MIN_INTERVAL_SECONDS`（默认约 0.8s），全局锁节流。
- **重试**：网络/412/429/5xx 等指数退避 + 抖动，次数由 `BILIBILI_MAX_RETRIES` 等控制。

### 接口顺序

1. `GET https://api.bilibili.com/x/web-interface/view?bvid=` — 取 `aid`、`pages`、标题、时长等。
2. `GET https://api.bilibili.com/x/player/wbi/v2?aid=&cid=&bvid=` — **优先**取字幕轨道列表（与 yt-dlp 一致，登录可见轨常在此）。
3. 若 `subtitles` 为空，再回退 `GET https://api.bilibili.com/x/player/v2`（部分稿件仅旧接口有轨，如部分 AI 字幕）。
4. 对每条轨道的 `subtitle_url` 再 **GET** 拉 JSON，`body[].content` 拼正文（`payload_to_text`）。

### 轨道选择与质量

- 轨道排序：中文类优先，其内简体/通用 zh 优先于繁体，再 AI 中文；同组内可匹配 `prefer_lang`（`_ordered_tracks`）。
- `BILIBILI_SUBTITLE_VALIDATE=true` 时：多轮采样可选；对每条下载结果做**时长覆盖**与**标题汉字二元组命中率**过滤，防止 AI 串台；AI 轨使用更高阈值（`BILIBILI_SUBTITLE_AI_MIN_TITLE_MATCH`）。
- `BILIBILI_SUBTITLE_VALIDATE=false` 时：更快，取首条非空；若开启 `BILIBILI_SUBTITLE_AI_SANITY_WHEN_VALIDATE_OFF`，仍可对 AI 轨做标题 sanity。
- 用户在前端**显式选语言**时：走 `only_lan` 分支，**不做标题命中率过滤**（仍可在 validate 开启时做时长覆盖）。

### 排错清单

- 轨道列表为空：检查 Cookie 是否完整、是否登录账号、分 P 是否正确。
- 正文空或校验全失败：尝试开启/关闭 `BILIBILI_SUBTITLE_VALIDATE`、调整采样轮次与间隔，或让用户指定 `lan`。
- 频繁 412/429：增大 `BILIBILI_MIN_INTERVAL_SECONDS`，避免并发多请求。

## 总结链路（TextSummaryService）

- 配置 `SUMMARY_ENABLED`、`SUMMARY_LLM_BASE_URL` 或 `SUMMARY_LLM_CHAT_COMPLETIONS_URL`、`SUMMARY_LLM_MODEL`；API Key 可用 `SUMMARY_LLM_API_KEY` 或 `OPENAI_API_KEY`（见 `app/core/settings.py` 别名）。
- 端点：若 `BASE_URL` 已以 `/chat/completions` 结尾则不再拼接；否则为 `{base}/chat/completions`。
- 请求体：OpenAI 兼容 `chat/completions`，`temperature` 来自 `SUMMARY_LLM_TEMPERATURE`。
- **短目标**（`max_chars <= 200`）：单段电报体中文；**长目标**：`## 总标题` + 若干 `**主题：**` 块（见 `summary.py` 内 prompt）。
- 正文入模上限约 **60000** 字符；响应解析支持 `message.content` 为字符串或多段 list；无有效 content 时回退 `_summarize_fallback`。

## 回归与自检

- 字幕大改后：在项目根执行 `python scripts/verify_subtitle_canary.py`（需 `.env` 中 `SESSDATA` 等，见 `CLAUDE.md`）。
- 全量测试：`pytest`。

## 打包给 OpenClaw 使用

将本目录 **`videototext` 整夹** 打成 zip（含 `SKILL.md`、`reference.md`、`code/`、`requirements-code.txt`）。解压后：

- Agent 阅读：`SKILL.md`、`reference.md`、`code/` 下源码。
- 若需本地运行子集：`pip install -r requirements-code.txt`，`PYTHONPATH` 指向 `code/`，`.env` 放在与 `SKILL.md` 同级目录（见 [code/README.md](code/README.md)）。

## 延伸阅读

- 环境变量逐项说明：[reference.md](reference.md)
