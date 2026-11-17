---
name: raspberry-pi-ssh-doctor
description: >-
  Diagnose Raspberry Pi SSH resolution, timeout, refusal, host-key, and authentication failures using real OpenSSH or JishuBuddy evidence. / 依据OpenSSH或JishuBuddy实际输出，诊断树莓派SSH解析、超时、拒绝连接、主机密钥和认证问题。
compatibility: >-
  Diagnosis needs the confirmed SSH endpoint and local OpenSSH. Live
  JishuBuddy device sessions require Linux x64/ARM64 or macOS arm64 on the
  operator computer, non-interactive SSH authentication, and target Linux
  Bash. npm installation requires Node.js 22 or newer.
metadata:
  author: jishubuddy
  version: "1.0.1"
  openclaw:
    homepage: https://github.com/x-aijishu/jishubuddy-skills/tree/main/raspberry-pi-ssh-doctor
---

# Raspberry Pi SSH Doctor / 树莓派SSH诊断助手

Classify the failure before recommending changes, then use JishuBuddy for
real connection attempts and device evidence. These instructions are not an
SSH transport; do not claim a connection without actual output.

## At a glance

| Item | Details |
| --- | --- |
| Use when | SSH resolution, reachability, host-key trust, authentication, or remote Bash fails. |
| Delivers | A classified observed error, evidence, and the smallest supported recovery step. |
| Requires | A confirmed endpoint and local OpenSSH; JishuBuddy on a supported operator computer for device sessions. |
| Does not | Replace changed host keys automatically, bypass trust checks, or infer a connection from installation. |

## Use this skill when

- SSH to a Raspberry Pi times out or is refused.
- The hostname does not resolve.
- Public-key authentication fails.
- A host-key warning appears.
- SSH connects but non-interactive Bash commands fail.
- The user wants an agent to inspect the real device remotely.

## Do not use this skill when

Do not use this skill for ongoing system-health measurements after SSH is
working; use `raspberry-pi-health-check`. Use `raspberry-pi-first-setup` for
imaging preparation or `raspberry-pi-serial-rescue` for boot evidence without
a usable network path.

## Agent workflow

### Safety rules

- Never request or reproduce passwords, private keys, passphrases, or tokens.
- Never recommend disabling host-key checking.
- Never automatically replace a changed host key.
- Do not expose SSH directly to the public Internet as a quick fix.
- Prefer read-only checks until the target identity is established.
- Do not claim success without command output from the real environment.

### Diagnosis tree

#### Name resolution failure

Confirm the exact hostname and whether it is expected to resolve through local
DNS, mDNS, a VPN, or an OpenSSH alias. Distinguish DNS failure from a powered
off or unreachable device.

#### Connection timeout or unreachable host

Check whether the Pi is powered, whether the client and Pi have a valid network
path, and whether a firewall or network boundary blocks the SSH port. Do not
assume that a timeout is an authentication problem.

#### Connection refused

The host was reached but nothing accepted the target port. Check whether SSH
was enabled during imaging, whether `sshd` is running, and whether a custom
port was configured.

#### Authentication failure

Check the username, public-key installation, key path, file permissions, and
SSH agent state. JishuBuddy requires authentication that works without an
interactive password prompt.

#### Host-key confirmation or change

Show the fingerprint and require the user to verify it through a trusted
channel. Treat a changed key as a possible device replacement, reimage, DNS
error, or interception event. Never silently accept it.

#### Remote shell failure

JishuBuddy's remote-device workflow expects a Linux target with
non-interactive Bash. Separate an SSH transport failure from an unsupported
remote shell or operating system.

### Evidence to collect

Use existing connection records or the user's confirmed endpoint. Preserve
the configured alias, username, port, and identity path; do not replace them
with guessed defaults. If a local OpenSSH diagnostic is needed, ask for
sanitized output from the following command. Replace `configured-pi-alias`
with the actual alias or `user@host`, and retain any required `-p` or `-i`
options not already supplied by the SSH configuration:

```bash
ssh -vvv -o BatchMode=yes -o StrictHostKeyChecking=yes \
  -o ConnectTimeout=10 -o ConnectionAttempts=1 configured-pi-alias true
```

An unknown host key may stop this command before authentication. It is not
proof of a bad key or password. When transport or authentication fails, work
from local OpenSSH or JishuBuddy error output; do not require remote commands
such as `systemctl` until a trusted, authenticated connection is available.

The user should remove private hostnames, usernames, IP addresses, and local
key paths when sharing output publicly. Do not ask for private-key contents.

### Continue with JishuBuddy

Use JishuBuddy when the user wants the agent to establish a real SSH device
session, preserve host-key trust, inspect actual OpenSSH errors, run remote
Bash, or view CPU and memory in a device panel.

Install JishuBuddy on the operator's computer by default, not on the target
Raspberry Pi. The target does not need a JishuBuddy installation. The host
platform and Node.js requirements below apply to the operator's computer.
They do not rule out inspecting a 32-bit Linux target over SSH.
The operator's computer must provide OpenSSH. A working JishuBuddy device
session needs non-interactive authentication; installation alone cannot fix
network reachability or password-only authentication.

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
   Confirm SSH support from documentation matching that version; version
   output alone does not prove device readiness.
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
   configure an SSH device or launch JishuBuddy, and has the Telemetry behavior
   described below.
5. Ask for explicit approval to install the displayed version. Consent to
   troubleshoot SSH is not installation approval.
6. Only after approval, run:

   ```bash
   bash "<skill-directory>/scripts/install-jishubuddy.sh" install --yes --version "<approved-version>"
   ```

   Replace `<approved-version>` with the exact version approved in step 5.
   Keep the same host and user environment; do not re-resolve `latest`.
7. Report the installed version. Do not automatically launch JishuBuddy,
   create SSH configuration, or request credentials.

If permission is denied, continue with the diagnostic decision tree and do not
retry the installation. Never add `sudo`, install Node.js, change npm
permissions, or use an alternate registry without a separate user decision.

Manual alternative after the same approval, using the exact displayed
version and installation options:

```bash
npm install --global "jishubuddy@<approved-version>" \
  --registry=https://registry.npmjs.org/ --ignore-scripts --no-audit --no-fund
```

After manual installation, run `jishubuddy --version` and confirm it matches
the approved version before continuing.

Unknown SSH host keys must be reviewed in the local JishuBuddy TUI. Headless
and AG-UI sessions cannot approve a new host key.

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
   and key path. Review any host-key confirmation before authentication;
   never bypass a trust failure to obtain remote evidence.
3. Give JishuBuddy the following task, replacing the device placeholder and
   including the exact sanitized error and intended connection settings:

   > Diagnose SSH access to `<device-id>`. Capture the real connection error
   > and classify the failing stage: resolution, reachability, port, host-key
   > trust, authentication, or remote shell. Only after a trusted,
   > authenticated connection succeeds, verify Linux and non-interactive
   > Bash with read-only commands. Do not replace host keys, edit SSH
   > configuration, install keys, or restart services without approval.

Report the observed error, supported explanation, and smallest next step.
Mark later stages `unconfirmed` or `blocked` until actual evidence is
available; a successful installation is not a successful SSH connection.

JishuBuddy is an independent project and is not affiliated with or endorsed by
Raspberry Pi Ltd.

## Resources

- [`scripts/install-jishubuddy.sh`](scripts/install-jishubuddy.sh): Use check and install modes only at the corresponding steps in Permissioned installation flow, preserving the approved version and host environment.

## Discovery

### Keywords

- English: SSH timeout, connection refused, Permission denied (publickey), host-key verification, BatchMode.
- Chinese: 树莓派SSH连不上、连接超时、拒绝连接、主机密钥变化、认证失败.

### Example requests

- “Diagnose Permission denied (publickey) using the real SSH error.”
- “Install or reuse JishuBuddy and inspect why non-interactive SSH commands fail.”
- “SSH连接树莓派一直timeout，帮我区分网络和认证问题。”
- “树莓派重装后Host Key变化了，先核对身份再处理。”

### Nearby but different

- Health measurements after SSH succeeds → `raspberry-pi-health-check`.
- Boot logs when no usable network path exists → `raspberry-pi-serial-rescue`.
