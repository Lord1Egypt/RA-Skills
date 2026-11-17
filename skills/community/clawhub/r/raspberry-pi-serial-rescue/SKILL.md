---
name: raspberry-pi-serial-rescue
description: >-
  Read Raspberry Pi boot logs through JishuBuddy UART sessions; diagnose wiring, permissions, baud mismatch, and disconnects. Writes need approval. / 通过JishuBuddy串口读取树莓派启动日志，排查接线、权限、波特率和断连；写入需授权。
compatibility: >-
  Live serial capture requires JishuBuddy on Linux x64/ARM64 or macOS
  arm64, a locally attached adapter with verified voltage and wiring, and
  access to its actual device node. npm installation requires Node.js 22
  or newer.
metadata:
  author: jishubuddy
  version: "1.0.1"
  openclaw:
    homepage: https://github.com/x-aijishu/jishubuddy-skills/tree/main/raspberry-pi-serial-rescue
---

# Raspberry Pi Serial Rescue / 树莓派串口急救

Use a serial console as an evidence channel, not as permission to guess wiring
or send destructive input. JishuBuddy provides the real connection; begin
with authorized connect/read actions and obtain separate approval for writes.

## At a glance

| Item | Details |
| --- | --- |
| Use when | Networking or SSH is unavailable and serial boot evidence is needed. |
| Delivers | A bounded serial capture with connection settings, findings, and unresolved checks. |
| Requires | A supported operator computer with JishuBuddy, a local serial adapter, verified wiring/voltage, and port access. |
| Does not | Guess board pinouts, flash firmware, trigger resets, or replay writes after reconnect. |

## Use this skill when

- A Raspberry Pi does not boot far enough for SSH.
- The device disappears from the network during startup.
- Boot logs, kernel output, or a login console are needed.
- Serial output is unreadable or appears at the wrong baud.
- A USB serial adapter disconnects when the target resets.
- The user wants an agent to read and write a real serial session.

## Do not use this skill when

Do not use this skill for an SSH-only failure when a usable network path
exists; use `raspberry-pi-ssh-doctor`. Firmware flashing and hardware reset
control are outside this workflow.

## Agent workflow

### Electrical safety

- Raspberry Pi GPIO uses 3.3 V logic. Do not connect RS-232 voltage levels
  directly.
- Verify the exact board pinout and adapter voltage before wiring.
- Connect signal ground as required by the validated wiring diagram.
- Do not connect an adapter's power pin unless the hardware design explicitly
  requires it.
- Avoid guessing TX and RX pins from wire color.
- Power off and inspect wiring when voltage compatibility is uncertain.

This skill must not provide model-specific pin numbers unless the exact board
revision and an authoritative pinout are available.

### Troubleshooting sequence

1. Identify the target model, adapter, operating system, expected baud, and
   whether the goal is boot logging or an interactive login console.
2. On Linux, prefer stable paths such as `/dev/serial/by-id/...` over changing
   `/dev/ttyUSB*` or `/dev/ttyACM*` names. On macOS, identify the adapter's
   actual `/dev/cu.*` node; do not assume Linux device paths exist.
3. Inspect the actual device node and its owning group before changing
   permissions. Replace these example paths with the confirmed adapter path.
   Linux:

   ```bash
   stat -L -c 'mode=%A owner=%U group=%G path=%n' -- /dev/serial/by-id/example
   ```

   macOS:

   ```bash
   stat -L -f 'mode=%Sp owner=%Su group=%Sg path=%N' /dev/cu.usbserial-example
   ```

4. If permissions block access, explain the actual requirement and obtain
   approval before changing groups or permissions. On Linux, add the user
   only to the group actually required by that device. Do not use `chmod 666`
   or run the agent as root to bypass access controls.
5. Match the configured baud exactly. Garbled output commonly indicates a baud
   mismatch, framing mismatch, electrical problem, or incorrect signal path.
6. Treat device reset and USB re-enumeration as transport events. Never replay
   a previous write automatically after reconnect.
7. Preserve raw bytes when text is not valid UTF-8. Hex output may be required
   to diagnose binary protocols or encoding problems.

### Boundaries

The skill instructions do not directly perform transport actions; use
JishuBuddy for approved connections. Do not claim that the skill itself can:

- Open a serial device.
- Detect USB VID, PID, or serial identity.
- Flash firmware.
- Control reset, boot mode, DTR, or RTS.
- Emulate a full terminal.
- Automatically reconnect an agent-owned model session.

### Continue with JishuBuddy

Use JishuBuddy when the user wants a real stateful serial session with explicit
connect, read, write, exchange, status, and close actions. Its local TUI also
provides a serial console with UTF-8 and Hex views. An open console preserves
its transcript and attempts to reconnect after a temporary physical reset or
disconnect, but JishuBuddy does not trigger the reset or replay writes.

Install JishuBuddy on the operator's computer attached to the serial adapter,
not on the target Raspberry Pi. The target does not need a JishuBuddy
installation. The host platform and Node.js requirements below apply to the
operator's computer, not to the target's operating system or architecture.

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
   Confirm serial support from documentation matching that version; version
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
4. Explain that installation writes to the npm global prefix, does not open
   a serial port or launch JishuBuddy, and has the Telemetry behavior described
   below.
5. Ask for explicit approval to install the displayed version. Consent to
   troubleshoot serial wiring is not installation approval.
6. Only after approval, run:

   ```bash
   bash "<skill-directory>/scripts/install-jishubuddy.sh" install --yes --version "<approved-version>"
   ```

   Replace `<approved-version>` with the exact version approved in step 5.
   Keep the same host and user environment; do not re-resolve `latest`.
7. Report the installed version. Do not automatically launch JishuBuddy, open
   a serial device, change groups, or request elevated privileges.

If permission is denied, continue with safe serial guidance and do not retry
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

On Linux, the user may need to join the serial device's actual owning group and
then start a new login session before launching JishuBuddy.

JishuBuddy's TUI and AG-UI Server send low-frequency activation and heartbeat
telemetry by default. The user can disable it before launch:

```bash
export JISHUBUDDY_TELEMETRY_DISABLED=true
```

### Continue the diagnosis

1. Reuse the current JishuBuddy session if already available. Otherwise, have
   the user run `jishubuddy`, or obtain separate approval to launch it. Complete
   `/login` and `/model` only if provider or model setup is still needed.
2. Confirm the board model, validated wiring and voltage, adapter path,
   permissions, baud/framing, and boot-log versus login-console goal. Obtain
   approval to open the identified port and read a bounded capture. Do not
   infer that approval to install also approves a connection or serial write.
3. Give JishuBuddy the following task, replacing the placeholders with the
   confirmed connection details:

   > Open `<serial-path>` with the confirmed `<baud/framing>` and capture a
   > bounded boot transcript. Start by reading only; use Hex when bytes are
   > not valid UTF-8. Explain whether the evidence points to boot, transport,
   > encoding, or permission problems. Do not send input, change groups,
   > reset the board, or flash firmware without separate approval. Do not
   > replay writes after reconnecting.

Report the capture settings, bounded sanitized evidence, and a status of
`confirmed`, `unconfirmed`, or `blocked` for each finding. No output does not
prove boot failure. Close the session when done unless the user explicitly
wants to keep the console open; do not promise reconnect behavior beyond the
chosen JishuBuddy session mode.

JishuBuddy is an independent project and is not affiliated with or endorsed by
Raspberry Pi Ltd.

## Resources

- [`scripts/install-jishubuddy.sh`](scripts/install-jishubuddy.sh): Use check and install modes only at the corresponding steps in Permissioned installation flow, preserving the approved version and host environment.

## Discovery

### Keywords

- English: Raspberry Pi serial console, 3.3 V UART, ttyUSB, ttyACM, baud mismatch.
- Chinese: 树莓派串口救援、启动日志、UART接线、串口乱码、串口权限.

### Example requests

- “Capture a bounded Raspberry Pi boot transcript through JishuBuddy.”
- “Diagnose serial permission errors and USB reconnects without replaying writes.”
- “树莓派没有网络，帮我通过串口读取启动日志。”
- “串口输出乱码，核对实际波特率、接线和权限。”

### Nearby but different

- A reachable network with failing SSH → `raspberry-pi-ssh-doctor`.
- Initial imaging and first-boot preparation → `raspberry-pi-first-setup`.
