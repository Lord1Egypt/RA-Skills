---
name: wechat-miniprogram-cloudbase-deploy
description: "WeChat Mini Program deployment onto WeChat CloudBase (云开发): deploy cloud functions via tcb, manually create database collections in the console, and upload the frontend via miniprogram-ci. Covers real-environment pitfalls: CLI cannot create collections, tcb fn invoke returns a Namespace metadata bug, the upload IP-whitelist only accepts IPv4 (so an IPv6 egress is always rejected), and the trial env defaults to ap-shanghai. Trigger when the task involves 部署微信小程序, 云开发, CloudBase, tcb 部署云函数, or miniprogram-ci 上传."
agent_created: true
---

# 微信小程序云开发部署

This skill documents the end-to-end deployment of a WeChat Mini Program whose
backend runs on WeChat CloudBase (云开发), including cloud functions (`tcb`),
the NoSQL database (collections), and the miniprogram frontend upload
(`miniprogram-ci`).

## When to use

- Deploying a Mini Program whose backend is (or will be) WeChat CloudBase.
- Migrating a self-hosted Express/SQLite backend to cloud functions + cloud DB.
- Uploading the miniprogram frontend to produce a 体验版 / 开发版.
- Diagnosing deploy failures: `collection not exists`, `GetFunction Namespace`,
  `errCode -10008 invalid ip`.

## Prerequisites (must be collected from the user first)

| Item | How the user obtains it | Why |
|---|---|---|
| Real **AppID** | MP backend → 开发 → 开发管理 → 开发设置 | `touristappid` cannot use CloudBase |
| **Env ID** | WeChat DevTools → 云开发 button → 环境设置 → 环境 ID (system-generated, looks like `xxx-4g1a2b3c`) | Target env for `tcb` deploy |
| **Subscribe template ID** | MP backend → 功能 → 订阅消息 → 我的模板 | For daily push `dailyPush` |
| **Upload private key** (`.key`) | MP backend → 开发设置 → 小程序代码上传密钥 → 生成/下载 | Required by `miniprogram-ci`. **Never paste key content into chat — use a local file path only.** |

Never ask the user to paste secret key contents. Read the path from disk.

## Deployment workflow

1. **Install CloudBase CLI into the managed node workspace** (avoid polluting
   the user's global env):
   ```
   cd ~/.workbuddy/binaries/node/workspace
   npm install @cloudbase/cli@latest
   ```
   The `tcb` binary lives at
   `node_modules/@cloudbase/cli/bin/tcb`.

2. **`tcb login`** — runs a device-code OAuth flow. Launch in background, scrape
   the authorization URL from `/tmp/tcb-login.log`, ask the user to open it and
   approve (confirm the shown `user_code`).

3. **Deploy cloud functions**:
   ```
   tcb fn deploy 函数名 --force -r ap-shanghai
   ```
   Deploy `api`, `login`, `seed`, `dailyPush` (or whatever the project defines).
   `wx-server-sdk` is installed in the cloud automatically.
   (Or run `scripts/deploy-cloud.sh` to batch-deploy all functions + seed in one command.)

4. **Create the 7 collections in the CloudBase console** (see Pitfall 1 — CLI
   cannot do this). Then invoke `seed` once:
   ```
   tcb fn invoke seed -r ap-shanghai
   ```
   Verify with `tcb db nosql execute --command '[...find gangs...]' -r ap-shanghai`.

5. **Upload the frontend** with `scripts/upload.js` from this skill (parameterized
   via env vars). See Pitfall 3 for the IP-whitelist trap.

## Critical pitfalls (detailed in references/pitfalls.md)

- **Pitfall 1 — Collections must be created in the console.** `tcb db create`
  was removed in CLI v3.8.1; `tcb api tcb CreateCollection` is offline; `tcb db
  nosql execute` INSERT writes to a *different* MongoDB instance invisible to
  `wx-server-sdk`; SDK `.add()` does NOT auto-create collections. Build a
  `seed` function that idempotently ensures collections + seed data.
- **Pitfall 2 — `tcb fn invoke` returns `GetFunction Namespace取值与规范不符`
  for most functions** (but `seed` succeeds). This is a CLI metadata bug in the
  CloudBase-namespace resolution; it does NOT affect the real
  `wx.cloud.callFunction` path. End-to-end verification must happen in WeChat
  DevTools, not via `tcb fn invoke`.
- **Pitfall 3 — Upload IP whitelist only accepts IPv4.** If the egress is IPv6
  (common when traffic routes through a local proxy like `127.0.0.1:xxxx`), the
  error is `errCode -10008 invalid ip: 该IPv6地址`. Whitelist UI cannot accept IPv6,
  so the only fix is to **turn off the whitelist toggle** in MP backend, or
  switch the machine to an IPv4 egress.
- **Pitfall 4 — `zsh` `PIPESTATUS` gotcha.** When chaining `node ... | tail`,
  `${PIPESTATUS[0]}` is misread in zsh; a non-zero exit can be masked as 0.
  Prefer the JS API (`ci.upload`) which returns a structured error object.
- **Pitfall 5 — Trial env is `ap-shanghai`.** Always pass `-r ap-shanghai` to
  `tcb` commands; `fn list` / `env list` work without it, but `invoke`/`deploy`
  need the region.

## Post-deploy, manual (compliance) actions only the user can do

| # | Action | Location |
|---|---|---|
| 1 | Fill 隐私保护指引 | MP backend → 设置 → 用户隐私保护指引 (required for review) |
| 2 | Create unique indexes | CloudBase console → 数据库 → 索引管理: `checkins{openid:1,date:1}`, `gang_memberships{openid:1,gangId:1}` |
| 3 | Verify subscribe field names | `dailyPush/index.js` `thing1/time2` must match the template's keyword order |
| 4 | Submit review → release | MP backend → 版本管理 (the only externally-visible, irreversible step) |

Note: uploading produces a 体验版 only — real users cannot see it. Review +
release is a separate, human-only action.
