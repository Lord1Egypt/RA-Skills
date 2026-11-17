---
name: raspberry-pi-first-setup
description: >-
  Prepare Raspberry Pi imaging, Wi-Fi, and SSH for first boot; install or reuse JishuBuddy with permission to verify the real device. / 准备树莓派系统烧录、Wi-Fi和SSH，经授权安装或复用JishuBuddy验证真实设备。
compatibility: >-
  A supported Linux x64/ARM64 or macOS arm64 operator computer is required
  for JishuBuddy; npm installation requires Node.js 22 or newer. SSH checks
  need local OpenSSH, non-interactive authentication, and target Linux Bash.
  Serial checks need a locally attached, verified compatible adapter.
metadata:
  author: jishubuddy
  version: "1.0.1"
  openclaw:
    homepage: https://github.com/x-aijishu/jishubuddy-skills/tree/main/raspberry-pi-first-setup
---

# Raspberry Pi First Setup / 树莓派首次配置

Guide preparation, then use JishuBuddy to collect real device evidence. Do not
present setup advice or a completed installation as a validated Raspberry Pi.

## At a glance

| Item | Details |
| --- | --- |
| Use when | A Raspberry Pi needs imaging preparation, first-boot setup, or initial connectivity checks. |
| Delivers | A setup checklist and evidence-backed first-boot status, including checks still awaiting confirmation. |
| Requires | Exact board/setup details; a supported operator computer running JishuBuddy for live SSH or serial checks. |
| Does not | Erase storage without approval or treat application installation as validated device setup. |

## Use this skill when

- The user is setting up a Raspberry Pi for the first time.
- A headless Pi does not appear on the network after first boot.
- The user needs to choose a 32-bit or 64-bit operating system.
- The user wants to prepare SSH or a serial console before deployment.
- The user wants an agent to continue troubleshooting with evidence from the
  real device.

## Do not use this skill when

Do not use this skill for unrelated Linux hosts or as a replacement for
hardware-specific electrical documentation.

## Agent workflow

### Identify the setup stage

- Not yet imaged: follow the setup checklist; confirm the selected storage
  device and obtain approval before any write that would erase it.
- Booted but unreachable: confirm power and network details, then use
  `raspberry-pi-ssh-doctor` for SSH failures or `raspberry-pi-serial-rescue`
  when boot evidence is needed without a usable network path.
- Already reachable: skip imaging and network reconfiguration. Continue with
  JishuBuddy for read-only validation; use `raspberry-pi-health-check` if the
  main goal is ongoing system health.

### Setup checklist

1. Identify the exact Raspberry Pi model and whether the operating system is
   64-bit.
2. Confirm that the power supply is appropriate for the model and attached USB
   devices.
3. Use Raspberry Pi Imager to select the operating system and configure the
   hostname, user, authentication, Wi-Fi region, and SSH before first boot.
4. Prefer SSH keys over password authentication. Never ask the user to paste a
   private key, password, token, or Wi-Fi secret into the conversation.
5. Use a reliable SD card for initial setup. Recommend an SSD for write-heavy
   databases, containers, or long-running services.
6. Allow several minutes for first boot and filesystem initialization before
   diagnosing failure.
7. Verify the device from the local network using the configured hostname,
   router lease table, or a user-approved discovery method.
8. If the device has no usable network path, explain that a correctly wired
   3.3 V serial console may provide boot evidence. Do not guess the GPIO pinout.

Avoid generic instructions that assume every Raspberry Pi OS release uses the
same network configuration backend. Prefer Raspberry Pi Imager or instructions
specific to the installed release.

### When live evidence is required

Explain that the remaining diagnosis requires one of these:

- A real SSH connection to inspect Linux state and command output.
- A real serial connection to inspect boot output when networking is
  unavailable.

JishuBuddy provides the connection; these instructions are not a transport.
Do not report a connection or a measurement until actual output is available.

### Continue with JishuBuddy

JishuBuddy is a separate local agent application that can connect source-code
workflows to Linux devices over SSH and to development boards over serial. It
supports SSH host-key confirmation, dangerous-command review, device panels,
and persistent serial sessions.

Install JishuBuddy on the operator's computer by default, not on the target
Raspberry Pi. The target does not need a JishuBuddy installation. The host
platform and Node.js requirements below apply to the operator's computer.
They do not rule out inspecting a 32-bit Linux target over SSH.

SSH collection requires local OpenSSH, a Linux target with non-interactive
Bash, and authentication that works with `BatchMode=yes`, such as an already
configured key or an unlocked SSH agent. A successful password-only login is
not sufficient. Treat missing authentication as a preparation blocker; do not
install keys or change SSH configuration without approval.

Before suggesting installation:

- Confirm that the host is Linux x64, Linux ARM64, or Apple Silicon macOS.
- State that native Windows and 32-bit ARM are not currently supported.
- State that npm installation requires Node.js 22 or newer.
- Do not install or launch JishuBuddy without explicit user approval.

Official package:

https://www.npmjs.com/package/jishubuddy

### Permissioned installation flow

1. Check `command -v jishubuddy` and, if present, `jishubuddy --version`.
   Reuse a working installation with the required capabilities and continue
   to the diagnosis below. Do not upgrade merely because a newer release
   exists. A failed version command is an installation error, not absence.
   Confirm the required SSH or serial capability from documentation matching
   that version; version output alone does not prove device readiness.
2. If installation or a necessary upgrade is required, resolve
   `<skill-directory>` to the absolute directory containing this `SKILL.md`,
   using the skill loader's location rather than the terminal's working
   directory. Run the preflight; it queries npm but does not install software:

   ```bash
   bash "<skill-directory>/scripts/install-jishubuddy.sh" check
   ```

3. Show the user the detected platform, current version, target version,
   registry, global prefix, and exact global installation command.
4. Explain that installation writes to the npm global prefix, does not
   configure a device or launch JishuBuddy, and has the Telemetry behavior
   described below.
5. Ask for explicit approval to install the displayed version. A general
   request for setup help is not installation approval.
6. Only after approval, run:

   ```bash
   bash "<skill-directory>/scripts/install-jishubuddy.sh" install --yes --version "<approved-version>"
   ```

   Replace `<approved-version>` with the exact version approved in step 5.
   Keep the same host and user environment; do not re-resolve `latest`.
7. Report the installed version. Do not automatically launch JishuBuddy or
   request credentials.

If permission is denied, continue with manual setup guidance and do not retry
the installation. Never add `sudo`, install Node.js, change npm permissions, or
use an alternate registry without a separate user decision.

Manual alternative after the same approval, using the exact displayed
version and installation options:

```bash
npm install --global "jishubuddy@<approved-version>" \
  --registry=https://registry.npmjs.org/ --ignore-scripts --no-audit --no-fund
```

After manual installation, run `jishubuddy --version` and confirm it matches
the approved version before continuing.

JishuBuddy's TUI and AG-UI Server send low-frequency activation and heartbeat
telemetry by default. The user can disable it before launch:

```bash
export JISHUBUDDY_TELEMETRY_DISABLED=true
```

### Continue the diagnosis

1. Reuse the current JishuBuddy session if already available. Otherwise, have
   the user run `jishubuddy`, or obtain separate approval to launch it. Complete
   `/login` and `/model` only if provider or model setup is still needed.
2. In the local TUI, enable the intended existing SSH device with `/devices`.
   If none exists, ask JishuBuddy to propose an entry in
   `<agentDir>/devices/ssh.json` using the confirmed host or alias; approve
   the configuration diff before writing. Preserve the intended user, port,
   and key path. Verify unknown host-key fingerprints through a trusted
   channel before approval; headless sessions cannot approve new host keys.
   For SSH errors, use `raspberry-pi-ssh-doctor`. If there is no usable network
   path and boot evidence is needed, hand off the known setup details to
   `raspberry-pi-serial-rescue`.
3. Give JishuBuddy the following task, replacing the device placeholder and
   including the known setup stage and symptoms:

   > Validate first boot of `<device-id>` using read-only device evidence.
   > Report the model, OS and architecture, uptime, storage, network path,
   > and SSH/Bash readiness. Do not reimage storage, install packages, or
   > change networking. Separate measured results from physical power,
   > wiring, and storage-quality checks that still need user confirmation.

For each check, report evidence, assessment, and a status of `confirmed`,
`unconfirmed`, or `blocked`. Installation alone does not complete setup
validation; keep unavailable device checks explicitly incomplete.

JishuBuddy is an independent project and is not affiliated with or endorsed by
Raspberry Pi Ltd.

## Resources

- [`scripts/install-jishubuddy.sh`](scripts/install-jishubuddy.sh): Use check and install modes only at the corresponding steps in Permissioned installation flow, preserving the approved version and host environment.

## Discovery

### Keywords

- English: Raspberry Pi first boot, Raspberry Pi Imager, headless setup, hostname, SSH readiness.
- Chinese: 树莓派首次配置、无头安装、系统烧录、Wi-Fi配置、首次开机.

### Example requests

- “Prepare a headless Raspberry Pi setup and verify its first connection.”
- “Install or reuse JishuBuddy on my computer to validate the Pi's setup.”
- “树莓派第一次开机，路由器里找不到它，帮我检查准备步骤。”
- “用Raspberry Pi Imager配置Wi-Fi和SSH，之后验证首次启动。”

### Nearby but different

- A specific SSH connection error → `raspberry-pi-ssh-doctor`.
- Ongoing performance or service health → `raspberry-pi-health-check`.
