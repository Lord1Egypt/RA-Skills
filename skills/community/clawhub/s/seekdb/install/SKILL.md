---
name: seekdb-install
description: Install / deploy a single SeekDB instance on the user's machine. Auto-detects OS and architecture, picks the right install method (Homebrew, Docker, yum, apt, Windows MSI, or pip embedded), and drives the install end-to-end — running commands, checking output, and diagnosing errors. Use when the user says "install seekdb", "deploy seekdb", "set up seekdb locally", "try seekdb on my machine", "use seekdb from Python", or asks how to get seekdb running on a specific OS.
compatibility: Linux x86_64/aarch64, macOS, Windows 10/11/Server 2022+. Embedded pip mode is Linux only.
metadata:
  author: oceanbase
  version: "1.0"
---

# Install SeekDB Locally

You are an **installation assistant** for OceanBase SeekDB. Your job is not just to show commands — you must **actively run commands**, check results, diagnose errors, and drive the installation to completion step by step.

Core principles:
- Run each command with the Bash tool and verify the output before proceeding.
- If a step fails, diagnose the cause and fix it before moving on. Do not just show the fix — execute it.
- Confirm each major milestone with the user before continuing to the next phase.
- Keep the user informed of what you are doing and why.

---

## Phase 1 — Detect environment

Run the following to understand the user's machine. Do this automatically without asking.

```bash
uname -s   # Darwin = macOS, Linux = Linux, MINGW64/MSYS/CYGWIN = Windows Git Bash
uname -m   # x86_64, aarch64, arm64
```

Also probe which package managers / runtimes are available:

```bash
command -v brew    # macOS Homebrew
command -v docker  # Docker
command -v yum     # RPM-based Linux
command -v apt     # DEB-based Linux
command -v pip     # Python pip
python3 --version  # Python version
```

From the results, infer the best installation options and present them to the user. For example:
- macOS detected → offer Homebrew and Docker
- Linux x86_64 with yum → offer yum/systemd and Docker
- Linux aarch64 with apt → offer apt/systemd and Docker
- Python 3.8+ found → also offer embedded pip mode
- Windows detected (MINGW64/MSYS/win32) → offer MSI installer

---

## Phase 2 — Confirm deployment mode

Ask the user which mode they want (if not already clear from context):

> "I can see you're on [OS]. Which mode would you like?
> - **Server mode** (Homebrew / Docker / yum / apt / Windows MSI) — runs a standalone server process
> - **Embedded mode** (pip install) — runs inside your Python process, no server needed (Linux only)"
>
> If on Windows, directly proceed to the Windows MSI flow (MSI is the only supported method).

---

## Phase 3 — Execute the chosen method

Pick the matching reference and follow it end-to-end. Each reference is self-contained: prerequisites, install steps, verification, and connection info.

| Method | Reference | Platforms |
|--------|-----------|-----------|
| Embedded (pip) | [references/pip-embedded.md](references/pip-embedded.md) | Linux x86_64, Linux aarch64 |
| macOS Homebrew | [references/macos-homebrew.md](references/macos-homebrew.md) | macOS 15+ |
| Docker | [references/docker.md](references/docker.md) | Linux, macOS |
| Linux yum (RPM) | [references/linux-yum.md](references/linux-yum.md) | Anolis 8/23, CentOS 7/9, openEuler 22/24 |
| Linux apt (DEB) | [references/linux-apt.md](references/linux-apt.md) | Debian 11/12/13, Ubuntu 20.04/22.04/24.04 |
| Windows MSI | [references/windows-msi.md](references/windows-msi.md) | Windows 10 (22H2+), 11, Server 2022+ |

---

## OS / method compatibility

| Method            | Linux x86_64 | Linux aarch64 | macOS | Windows x86_64 |
|-------------------|:---:|:---:|:---:|:---:|
| pip (embedded)    | ✅  | ✅  | ❌  | ❌  |
| yum / systemd     | ✅  | ✅  | ❌  | ❌  |
| apt / systemd     | ✅  | ✅  | ❌  | ❌  |
| Docker            | ✅  | ✅  | ✅  | ❌  |
| Homebrew          | ❌  | ❌  | ✅  | ❌  |
| MSI / Windows Svc | ❌  | ❌  | ❌  | ✅  |

---

## References

- Deploy by systemd: <https://docs.seekdb.ai/seekdb/deploy-by-systemd/>
- pyseekdb embedded install: <https://docs.seekdb.ai/seekdb/pyseekdb-sdk-get-started/#install-pyseekdb>
- Docker image: <https://github.com/oceanbase/docker-images/blob/main/seekdb/README.md>
- Windows MSI download: <https://mirrors.oceanbase.com/oceanbase/community/stable/windows/11/x86_64/seekdb-1.3.0.0-win64.msi>
- Full documentation: <https://www.oceanbase.ai/docs/seekdb-overview/>
