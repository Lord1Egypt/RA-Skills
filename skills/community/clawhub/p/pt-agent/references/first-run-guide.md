# First-Run Guide

Use this reference when the user is new, asks to initialize, or requests search/download/status without a usable tracker or downloader.

## Contents

- Goal
- First Action
- User Journey
- Secure Credential Setup
- Validation
- Completion

## Goal

Reach one working tracker-to-downloader loop with the fewest interruptions. Preserve the user's original request and resume it after setup.

## First Action

Read existing state before asking questions. Prefer the host config summary; otherwise execute the bundled runtime from the resolved skill root:

```bash
python3 "$SKILL_ROOT/scripts/pt_runtime.py" first-run
```

Do not lead normal onboarding with storage paths, commands, JSON, adapter ids, or capability names.

## User Journey

When nothing is configured, acknowledge the user's goal and ask for the first decision only:

```text
我会先帮你接入一个 PT 站点，再连接下载器；完成后继续刚才的任务。

你现在有哪种接入方式？
1. Prowlarr、Jackett 或 Torznab（推荐，最稳定）
2. 已登录该站点的浏览器会话
3. 已放在密码管理器或环境变量中的站点凭据
4. 站点提供的 RSS

告诉我选项和站点名即可。不要在聊天里发送 Cookie、密码或 passkey。
```

If a tracker draft exists, summarize what is already known and ask only for the missing decision:

```text
我找到了 {displayName} 的未完成配置，站点地址和接入方式已经记住。
现在只差安全凭据来源：使用已登录浏览器，还是你已有的密码管理器/环境变量？
```

If the tracker is usable but no downloader exists:

```text
站点已经可以使用。下一步连接下载器。
请告诉我下载器类型（qBittorrent 或 Transmission）和访问地址；密码不要发到聊天里。
```

If both are usable, skip setup and continue the user's original search, status, or handoff request.

## Secure Credential Setup

Prefer the host's secret store or authenticated browser profile. If neither exists, guide the user to place the value in an environment variable outside chat, then store only its `env://NAME` reference.

Use technical reference names only after the user selects a method or explicitly asks for implementation details. Safe stored forms include:

```text
profile://trackers/site-a
secret://trackers/site-a/cookie
env://SITE_COOKIE
env://QB_CREDENTIALS
```

Never accept these as config values:

```text
Cookie: ...
passkey=...
username:password
download.php?id=...&passkey=...
```

If a secret appears in chat, do not quote it. Explain that it was exposed, recommend rotation when appropriate, and continue only with a replacement reference.

For `env://QB_CREDENTIALS`, the environment value may contain qBittorrent's `username:password`, API key, or username/password JSON. The environment value is resolved only at runtime and must never be copied into config or output.

## Validation

For a tracker:

1. Resolve the preset and adapter.
2. Validate the chosen auth mode and reference fields.
3. Show a redacted summary and ask once for confirmation.
4. Save the configuration, then run a harmless health check when the reference can be resolved.
5. Fetch sanitized account statistics when supported.

For a downloader:

1. Validate type, trusted address, credential reference, and default save behavior.
2. Show a redacted summary and ask once for confirmation.
3. Save it and run a status check.

If runtime validation is unavailable, say what was statically validated and mark the configuration for a later health check. Do not describe a provider limitation as a bad password.

## Completion

Return to the user's goal instead of ending on setup mechanics:

```text
初始化完成。
- 站点：{displayName}，登录状态正常
- 下载器：{downloaderName}，连接正常

我现在继续搜索“{originalQuery}”。
```

When there was no pending task, offer a few natural next actions such as searching, viewing account status, or checking the downloader queue.
