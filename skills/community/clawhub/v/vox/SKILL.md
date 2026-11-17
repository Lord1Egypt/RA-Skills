---
name: vox
description: Use only when the current user explicitly asks to use Vox to transcribe one URL written in the request or one exact local audio/video file path, or explicitly asks for Vox CLI or Vox Skill install, status, authentication, or troubleshooting. Do not trigger from a mere Vox mention, an implicit attachment, directory contents, a glob, stdin, a batch request, or inferred permission to read files, authenticate, install software, or write output.
user-invocable: true
disable-model-invocation: true
metadata:
  openclaw:
    requires:
      bins:
        - vox
---

# Vox

Use the installed `vox` CLI instead of the web UI.

## Keep authorization explicit

- Act only on one URL written by the current user or one exact local file path the current user identified.
- Never browse a directory, inspect nearby files, read the clipboard, infer an attachment, expand a glob, consume stdin, or assemble a batch to choose an input.
- Treat install, login, logout, configuration changes, file reads, and output writes as separate actions that require the current request to authorize them.
- Keep `vox auth status` and `vox skill status` read-only. Troubleshooting permits read-only diagnosis only.

## Check the CLI

Prefer the installed `vox` command. Check it with:

```bash
command -v vox
vox --version
vox --help
```

Require CLI `0.1.0` or newer and explicit `auth`, `transcribe`, and `skill` commands. If it is missing or too old, ask before installing or upgrading:

```bash
npm install -g @casatwy/vox@latest
```

Do not fall back to another product's CLI, environment variables, or configuration.

## Authenticate safely

Run `vox auth status` before asking for credentials. If login is needed, direct the user to create a key at `https://vox.reka.cc/me/api-keys`, then run:

```bash
vox auth login
```

Let the CLI read the key through its hidden interactive prompt. Never put a key in command arguments, a copied command, chat output, a log, or a file created by the agent. Automation may use an already-provided `VOX_API_KEY` environment variable, but never print it.

Use the production default for normal work. Do not pass `--base-url` or set `VOX_BASE_URL` unless the current user explicitly requests a different Vox endpoint.

## Transcribe exactly one input

For a URL, pass the exact submitted URL unchanged and let Vox identify whether the backend can transcribe it:

```bash
vox transcribe '<url>'
```

For one exact ordinary local audio/video file, use:

```bash
vox transcribe --file '<path>'
```

Add `--mime-type '<type>'` only when the current user supplies the type or automatic detection fails and the user confirms the correction.

- Do not maintain, enumerate, or infer a source allowlist.
- Do not rewrite the URL into another source or search for a replacement.
- Reject directories, globs, stdin, special files, multiple inputs, batches, and resumable-upload expectations.
- Do not retry unsupported collections, non-transcribable posts, paid-only content, or other HTTP 422 audit results.

## Preserve user choices

- Omit `--language` unless the current user explicitly selects a transcription language. Do not infer it from the conversation, locale, title, or media.
- Add `--format '<format>'` only for an explicitly requested format.
- Add `--output '<path>'` only when the user explicitly requests a destination. Never authorize overwrite; preserve the CLI's no-clobber result.
- Keep transcript/result bytes on stdout or in the requested output file. Summarize progress from stderr without pasting raw diagnostic or JSONL events.
- Use text progress for people and JSONL only when a calling workflow explicitly needs machine-readable progress.

## Handle results and failures

- Preserve SRT, VTT, JSON, JSONL, and explicitly requested raw text exactly. Do not clean, translate, summarize, or reformat them.
- Report when the service returns subtitles directly instead of creating a paid transcription.
- Treat authentication failures, insufficient balance, and HTTP 422 responses as terminal. Do not retry them.
- Allow the CLI to perform its bounded retry and SSE-to-polling recovery. Never create a second task merely because live events stop.
- On `SIGINT`, say only that local waiting stopped. Do not claim the server task was cancelled.
- Never expose API keys, cookies, signed URLs, secret query parameters, private API payloads, or another product's configuration while diagnosing a failure.

## Manage the Skill

Only on an explicit install request, use one platform value:

```bash
vox skill install --platform codex
vox skill install --platform claude
vox skill install --platform gemini
vox skill install --platform openclaw
```

Use `vox skill status` for read-only discovery. Add `--platform codex|claude|gemini|openclaw` only when the user names one platform. Refuse to replace an existing same-name installation from a different source; surface the conflict and stop.

## 来源与合集

支持 Bilibili、抖音、小红书、小宇宙、喜马拉雅、YouTube、Apple Podcasts、Twitter/X、TikTok、Instagram、微信视频号、微信公众号、红果、研直播、超星、快手、腾讯视频、看看新闻 共 18 个命名平台，以及 HTTP/HTTPS 通用媒体链接、单文件上传，共 20 类来源。视频号遵循独立功能开关。网页上传公开可见，`/upload` 保持 noindex，不进入 sitemap。

红果整剧、抖店多课时与网页多媒体候选须先选一项，不默认选择，不批量转写。红果选集失败可返回目录重新选择；候选过期须重新解析。YouTube 播放列表、B站合集、小宇宙节目、Apple Podcasts 节目、喜马拉雅专辑和网页 playlist 只展示真实摘要并引导具体单集；抖音与小红书作者页展示作者摘要并引导具体作品。带 list 的 YouTube 具体视频仍按单视频处理。付费或受限内容先分类，所有摘要、未选目录和不可转写内容均不得复用、扣分钟或创建任务。封面缺失或加载失败隐藏；未知集数与零条区分。

CLI 摘要型合集返回 HTTP 422、`UNSUPPORTED_CONTENT` 和 `mode`；旧 `COLLECTION_UNSUPPORTED` 仅保留读取兼容。多媒体候选返回 `MULTIPLE_MEDIA_SELECTION_REQUIRED`；红果目录返回 `HONGGUO_EPISODE_REQUIRED`，附归属当前用户的 `parseToken`，引导网页选集或提交精确单集 URL。token 不允许跨用户使用。
