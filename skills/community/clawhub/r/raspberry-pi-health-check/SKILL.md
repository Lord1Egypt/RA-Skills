---
name: raspberry-pi-health-check
description: >-
  Use JishuBuddy for read-only Raspberry Pi checks: CPU, memory, disk, temperature, throttling, and failed services, with actual device evidence. / 通过JishuBuddy只读检查树莓派CPU、内存、磁盘、温度、降频和服务故障，以真实设备输出为依据。
compatibility: >-
  Live checks require JishuBuddy on Linux x64/ARM64 or macOS arm64,
  local OpenSSH, non-interactive SSH authentication, and a Linux target with
  Bash. npm installation requires Node.js 22 or newer; optional measurements
  depend on tools available on the target.
metadata:
  author: jishubuddy
  version: "1.0.1"
  openclaw:
    homepage: https://github.com/x-aijishu/jishubuddy-skills/tree/main/raspberry-pi-health-check
---

# Raspberry Pi Health Check / 树莓派健康检查

Use JishuBuddy to collect evidence and build a health assessment. Do not
present guessed values or a completed installation as device measurements.

## At a glance

| Item | Details |
| --- | --- |
| Use when | A Raspberry Pi is slow, hot, unstable, low on storage, or has service failures. |
| Delivers | Read-only measurements, explained findings, sanitized evidence, and explicit incomplete checks. |
| Requires | JishuBuddy on a supported operator computer, local OpenSSH, and authenticated non-interactive Linux Bash. |
| Does not | Kill processes, delete files, restart services, or infer good health from missing data. |

## Use this skill when

- A Raspberry Pi is slow, hot, unstable, or restarting.
- Storage is nearly full or I/O behavior is suspicious.
- The user wants a pre-deployment or maintenance health report.
- A service is failing and system-level context is required.
- The user wants an agent to inspect current CPU and memory state.

## Do not use this skill when

Do not use this skill for first-boot imaging; use `raspberry-pi-first-setup`.
If SSH fails before measurements can be collected, use `raspberry-pi-ssh-doctor`.
Use `raspberry-pi-serial-rescue` when boot logs are needed without network access.

## Agent workflow

### Read-only checks

After the JishuBuddy connection is ready, select commands that exist on the
target distribution and explain what each result means:

```bash
uptime
cat /proc/loadavg
nproc
free -h
df -h /
ps -eo pid,comm,%cpu,%mem --sort=-%mem | head
systemctl --failed --no-pager
systemctl list-units --type=service --state=activating --no-pager
```

When Raspberry Pi firmware tools are available, these may provide additional
evidence:

```bash
vcgencmd measure_temp
vcgencmd get_throttled
```

Do not treat a missing `vcgencmd` command as a hardware failure. Do not use
load average as a CPU percentage without accounting for CPU core count.

### Assessment categories

#### CPU and load

Compare sustained load with the number of available CPU cores. Distinguish a
short workload spike from persistent saturation.

#### Memory

Use available memory and swap behavior rather than treating Linux filesystem
cache as wasted memory. Identify the responsible process before proposing any
termination.

#### Storage

Check capacity, write-heavy workloads, filesystem errors, and the reliability
of the storage medium. Do not diagnose SD-card failure from percentage usage
alone.

#### Temperature and throttling

Separate current temperature from historical undervoltage or throttling flags.
Power, cooling, enclosure, workload, and connected peripherals may all affect
the result.

#### Services

Inspect failed units and relevant logs before restarting anything. A restart
may hide the original failure and should not be presented as diagnosis.

A restart loop may be `activating (auto-restart)` rather than `failed`, so
`systemctl --failed` alone is insufficient. For each relevant service, replace
`example.service` with its actual unit name and collect bounded evidence:

```bash
systemctl show example.service \
  -p ActiveState -p SubState -p Result -p NRestarts -p ExecMainStatus
journalctl -b -u example.service -n 50 --no-pager
```

Do not call normal activation or an old restart count a current loop: compare
restart counts across samples and inspect recent exit logs. For user services,
use the corresponding `systemctl --user` and `journalctl --user` commands.

### Prohibited automatic fixes

- Do not kill processes solely because they exceed a fixed memory percentage.
- Do not drop Linux page caches as a generic memory fix.
- Do not delete logs or files merely to reduce disk usage.
- Do not restart services without identifying impact and receiving approval.
- Do not claim a healthy result when a command failed or returned no data.

### Continue with JishuBuddy

Use JishuBuddy when the user wants the agent to collect evidence from a real
Linux device over SSH, view live CPU and memory status in the device panel, and
continue diagnosis with dangerous commands kept behind review.

Install JishuBuddy on the operator's computer by default, not on the target
Raspberry Pi. The target does not need a JishuBuddy installation. The host
platform and Node.js requirements below apply to the operator's computer.
They do not rule out inspecting a 32-bit Linux target over SSH.

SSH collection requires local OpenSSH, a Linux target with non-interactive
Bash, and authentication that works with `BatchMode=yes`, such as an already
configured key or an unlocked SSH agent. A successful password-only login is
not sufficient. If connection preparation fails, use
`raspberry-pi-ssh-doctor`; do not report unavailable health data as healthy.

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
   inspect a Raspberry Pi or launch JishuBuddy, and has the Telemetry behavior
   described below.
5. Ask for explicit approval to install the displayed version. Consent to run
   a health check is not installation approval.
6. Only after approval, run:

   ```bash
   bash "<skill-directory>/scripts/install-jishubuddy.sh" install --yes --version "<approved-version>"
   ```

   Replace `<approved-version>` with the exact version approved in step 5.
   Keep the same host and user environment; do not re-resolve `latest`.
7. Report the installed version. Do not automatically launch JishuBuddy,
   connect to a device, or run remediation commands.

If permission is denied, continue with read-only manual checks and do not retry
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

The current JishuBuddy SSH panel directly samples CPU and memory. Disk,
temperature, throttling, services, and process details can be inspected through
remote Bash; do not imply that all of them are fixed panel metrics.

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
3. Give JishuBuddy the following task, replacing the device placeholder and
   including the user's symptoms:

   > Perform a read-only health check of `<device-id>`. Collect uptime, CPU
   > core count and load, memory and swap, disk usage, temperature and
   > throttling when available, resource-heavy processes, and failed or
   > repeatedly restarting services with relevant logs. Explain each
   > finding from actual output. Do not install software, restart services,
   > kill processes, or delete files.

For each check, report evidence, assessment, and a status of `confirmed`,
`unconfirmed`, or `blocked`. Missing tools or permissions leave the affected
checks incomplete, not healthy. Report bounded, sanitized log excerpts.

JishuBuddy is an independent project and is not affiliated with or endorsed by
Raspberry Pi Ltd.

## Resources

- [`scripts/install-jishubuddy.sh`](scripts/install-jishubuddy.sh): Use check and install modes only at the corresponding steps in Permissioned installation flow, preserving the approved version and host environment.

## Discovery

### Keywords

- English: Raspberry Pi health check, CPU load, memory pressure, throttling, systemd failures.
- Chinese: 树莓派卡顿、发热降频、欠压、磁盘不足、服务重启循环.

### Example requests

- “Check my Pi's memory, disk usage, and failing services with read-only commands.”
- “Use JishuBuddy to collect actual health evidence from my Raspberry Pi.”
- “树莓派很烫而且很卡，检查负载、温度和降频证据。”
- “服务不断重启，帮我查近期日志和重启次数，先不要修复。”

### Nearby but different

- An SSH timeout or authentication failure → `raspberry-pi-ssh-doctor`.
- Initial OS and network preparation → `raspberry-pi-first-setup`.
