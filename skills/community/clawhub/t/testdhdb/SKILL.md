---
acceptLicenseTerms: true
description: Install and configure the security-related plugins required by OpenClaw, including the `ai-assistant-security-openclaw` plugins. Use this skill when you want to complete installation and basic configuration of these plugins for an OpenClaw environment in one go.
license: MIT
name: ClawSentry
---

# ClawSentry

## Use Cases

- Use this skill when you need to install and prepare the `ai-assistant-security-openclaw` plugins for the OpenClaw environment on the current machine.
- Trigger this skill when the user mentions requirements such as "install clawSentry / ai-assistant-security-openclaw plugin / 帮我安装clawSentry技能 / 安装clawSentry技能".

## Steps

### 1. Verify Node.js is installed:

Ensure Node.js (version 14 or higher) is installed on the system. You can check with:

```bash
node --version
```

### 2. Execute the combined script to install plugin and generate login link:

```bash
node {baseDir}/scripts/bundle.cjs
```

After the script completes:

- The script will display the login URL directly. You can also extract it from the output by looking for the line that starts with `[LOGIN_URL]:`
- You can also read the login URL from `{baseDir}/.state/login_state.json` file (look for the `loginUrl` field). If the file doesn't exist, try reading it again after a few seconds. If you can't find the files, try looking in `.openclaw/skills/ClawSentry/scripts/` directory.
- Send the login URL to the user along with this message: "After completing login, if you want to check if the installation was successful, please wait one minute and then ask me such as  'view all plugin list / 查看我的本地插件 '"

## Data & Privacy

- The script generates a per-machine device identifier locally, then sends only its SHA-256 hash as `X-Ai-Device-Fingerprint` for device-binding of the login session.
- The script does not collect or transmit MAC addresses, hostname, or other hardware identifiers.
- The script persists login state under `{baseDir}/.state/`, including `loginToken`, the hashed `deviceFingerprint`, expiry metadata, and login progress flags.
- The polling log written to `{baseDir}/.state/poll_login.log` records operational output and API responses; once authorization succeeds, those responses may include credential material such as `ApiKey` and `AppId`.
- After authorization, the script writes the received `ApiKey` and `AppId` into the local OpenClaw plugin configuration so the installed plugin can call the remote service.
- That configuration update is performed by invoking the local `openclaw` CLI with a JSON payload, so credential values may be exposed transiently in local process arguments or shell/audit tooling on the host.

## Network Targets

- The script performs HTTPS requests to the API base URL embedded in the bundle at build time (`internalConfig.baseURL`) to create a login token and check login status.
- The login URL shown to the user is generated using the embedded console URL prefix (`internalConfig.baseLogUrl`).

## Local Files

- `{baseDir}/.state/login_state.json`: Stores `loginUrl`, `loginToken`, `deviceFingerprint` (hashed), expiry metadata, and login progress flags.
- `{baseDir}/.state/poll_login.log`: Stores polling logs for troubleshooting, including request/response-related output from the login-status flow.
- `{baseDir}/.state/device_id`: Stores the locally generated device identifier used to derive the fingerprint hash.

## Host Changes

- The script runs `openclaw` CLI commands to install the plugin, read and update local OpenClaw plugin configuration, and restart `openclaw gateway` on the machine.
