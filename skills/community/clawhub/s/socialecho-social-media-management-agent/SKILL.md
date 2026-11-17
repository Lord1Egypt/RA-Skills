---
name: socialecho-social-media-management-agent
description: Use SocialEcho OpenAPI for explicit team/account/content queries and user-authorized TikTok Shop sync or cross-platform publishing. Requires a user-provided Team API Key and confirmation before live writes.
---

# SocialEcho Social Media Management Agent

Use this skill to call SocialEcho external APIs with a team API key. Send network requests only to `https://api.socialecho.net`, or to `https://api-dev.socialecho.net` when the user explicitly targets development.

## Authorization boundary

- Accept the Team API Key only when the user explicitly supplies it for this task. Never search environment variables, credential stores, shell history, or files for a key. Never print or persist the key.
- Team, account, OAuth-link, article, report, upload-URL, Reddit, Pinterest, product, genre, and music-list calls are read or preparation operations. Run only those needed for the user's request.
- Product sync and article publishing are live writes. Before either write, show the exact target account and relevant payload summary, including content, attachments, settings/privacy, and immediate or scheduled timing. Obtain explicit user authorization for that exact action in the current request.
- Do not infer write authorization from API access, a previous action, a broad request to manage social media, or an earlier conversation. Never add `--execute` on the user's behalf without current explicit authorization.
- Dry runs make no network request. Execute a live write only with both `--execute` and a matching `--confirm-account-id`.

## Prerequisites

1. Sign up / sign in at `https://app.socialecho.net/`.
2. Create a team.
3. In Team Management, create an API key.
4. Use explicit CLI options for auth/runtime (do not auto-read env vars):
   - `--api-key` (required)
   - `--base-url` (optional; only the SocialEcho production or development API host is accepted, default `https://api.socialecho.net`)
   - `--team-id` (optional; maps to `X-Team-Id` when set)
   - `--lang` (optional, default `zh_CN`)

## Setup

```bash
cd socialecho-skills
npm ci
```

Runtime requirement: Node.js `>=18`

## Commands

查询接口统一使用 **GET + QueryString**。GET 不得携带 body；CloudFront 会对带 body 的 GET 直接返回 `403`：

```bash
./team.js --api-key YOUR_KEY
./account.js --api-key YOUR_KEY --page 1 --type 1
./oauth-links.js --api-key YOUR_KEY
./article.js --api-key YOUR_KEY --page 1 --account-ids 41,42
./report.js --api-key YOUR_KEY --start-date 2026-01-01 --end-date 2026-03-24 --time-type 1 --group day --account-ids 41,42
```

上传准备与平台查询：

```bash
./upload-url.js --api-key YOUR_KEY --content-type image/png
# 或: --content_type video/mp4
./reddit-communities.js --api-key YOUR_KEY --account-id 163751
./pinterest-boards.js --api-key YOUR_KEY --account-id 163751
./tiktokshop-products.js --api-key YOUR_KEY --account-id 43 --page 1 --per-page 20
./tiktokshop-music-genres.js --api-key YOUR_KEY
./tiktokshop-music-trending.js --api-key YOUR_KEY --account-id 43 --country-code US --genre BGM --date-range 7DAY
```

实时写入操作先执行不带认证信息的 dry-run，向用户展示预览；获得当前操作的明确授权后，再使用双重确认参数：

```bash
./publish-article.js --payload ./publish-payload.example.json
./publish-article.js --api-key YOUR_KEY --payload ./publish-payload.example.json --execute --confirm-account-id 163751
./tiktokshop-product-sync.js --account-id 43
./tiktokshop-product-sync.js --api-key YOUR_KEY --account-id 43 --execute --confirm-account-id 43
```

`GET /v1/upload/url` 的 QueryString **必须** 包含 `content_type`（与实际上传文件一致的 MIME）。**允许值**为：`image/jpeg`、`image/jpg`、`image/png`、`image/gif`、`image/webp`、`image/bmp`；`video/mp4`、`video/avi`、`video/mov`、`video/wmv`、`video/flv`、`video/webm`、`video/mkv`、`video/3gp`、`video/quicktime`。

`publish-article` 的请求体字段以仓库内 `openapi.json` / `openapi.yaml` 中 `POST /v1/publish/article` 为准；请准备完整 JSON 文件并通过 `--payload` 传入。Dry-run 只读取指定 payload 文件并输出目标摘要，不读取其他文件，也不调用网络。

选中 TikTok/TikTok Shop 音乐时，`extra.music` 必须完整包含 `url`、`uuid`、`cover`、`title`、`artist`、`duration`、`selection`、`music_volume`、`original_sound_volume` 九个字段。

## Platform publish limits (copy, media, formats)

各平台文案长度、媒体数量、格式与尺寸等**发布前校验规则**见同目录 Markdown（与帮助中心内容对齐，供集成与运营参考）：

| File | Language |
| --- | --- |
| `platform-publish-limits_cn.md` | Chinese |
| `platform-publish-limits_en.md` | English |

**CLI：在终端打印全文到 stdout（便于管道保存或查阅）：**

```bash
node ./platform-limits.js
node ./platform-limits.js --lang en
# 若已全局安装本包：
# socialecho-platform-limits
# socialecho-platform-limits --lang en
```

## Notes

- 成功判定：HTTP `2xx` 且响应 JSON 的 `code` 为 `0`。
- GET 参数全部通过 QueryString 传递；数组使用 `account_ids[]=1&account_ids[]=2`。
- 外部 API 限流：单 Key 建议不超过 **120 次/分钟**；循环调用请加节流与退避。
- 规范文件：仓库根目录同步的 `默认模块.openapi.json` 与 skill 内 `openapi.json` / `openapi.yaml` 内容一致（便于 Clawhub / GitHub 与 Agent 阅读）。
