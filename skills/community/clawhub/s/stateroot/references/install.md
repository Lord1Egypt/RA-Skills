# Install (official assets)

Authoritative: https://stateroot.dev/docs/getting-started/installation  
Releases: https://github.com/CognizTech/stateroot/releases

Do not invent other download URLs. Current tagged releases ship **Linux x64 and ARM64**, **Windows x64**, and **macOS Apple Silicon** binaries. One binary, no extra runtime.

## Linux

```bash
curl -sSfL https://github.com/CognizTech/stateroot/releases/latest/download/install.sh | sh
```

Selects `stateroot-linux-x64` or `stateroot-linux-arm64` for the host, verifies SHA-256 against `checksums.txt` (fail closed), and installs to `~/.local/bin`. Needs glibc 2.17 or newer (Ubuntu 16.04, Debian 9, RHEL 7, and later).

If `command not found: stateroot` after a successful install, add `~/.local/bin` to `PATH` and retry in a new shell.

The installer may also run `stateroot install` (global harness hooks). Still run **`stateroot setup`** after a fresh install — that is identity + harnesses + skills, not an optional extra.

## Windows

Prefer the MSI: https://github.com/CognizTech/stateroot/releases/latest/download/StateRootSetup-x64.msi

PowerShell:

```powershell
irm https://github.com/CognizTech/stateroot/releases/latest/download/install.ps1 | iex
```

`stateroot-windows-x64.exe` is the portable CLI, not an installer.

## macOS (Apple Silicon)

```bash
curl -sSfL https://github.com/CognizTech/stateroot/releases/latest/download/install.sh | sh
```

The installer selects `stateroot-macos-aarch64`, verifies it against `checksums.txt`, and installs it to `~/.local/bin`.

Intel Macs do not currently have a release binary. Build from source:

```bash
git clone https://github.com/CognizTech/stateroot.git
cd stateroot
cargo install --path stateroot-cli
```

Requires Rust 1.85+ and a C toolchain. Alternative: `cargo build --release -p stateroot-cli` → `target/release/stateroot`.

## Verify

```bash
stateroot --version
stateroot doctor
```

`doctor` is local diagnostics only. It is designed to pass on a fresh machine with zero config and zero API keys. Non-zero exit means broken local setup — quote the output. Missing optional synthesis keys is not a failure.

## Update (after bootstrap)

Not this skill's job once setup has run. The built-in skill / CLI owns daily use. For reference only:

```bash
stateroot self-update
stateroot self-update --check
stateroot self-update --tag nightly
stateroot self-update --tag v0.2.14
stateroot self-update --check --tag nightly
```

`self-update` follows the running binary's channel: a production build follows the latest production release, and a dev/nightly build follows `nightly`. Background updates retain that channel too. `--tag nightly` explicitly selects the rolling preview from `main`; `--tag v0.2.14` explicitly selects that production release, including switching back from nightly. Updates re-arm harness integrations and refresh editor release metadata automatically.

If a public GitHub API quota is exhausted, current clients use published release metadata with checksum verification. A GitHub account or token is optional; a `403` alone does not prove a rate limit.

To add integrations introduced since setup, update the CLI and rerun `stateroot install`; identity setup does not need to be reset.

Opt out: `STATEROOT_NO_AUTO_UPDATE=1`.

## Uninstall

```bash
stateroot uninstall          # integrations + config; project .stateroot/ kept
stateroot uninstall --purge  # also delete ~/.stateroot
```

`--purge` is the only way the CLI deletes user-global identity. Project folders are never touched by uninstall — that is `stateroot remove` inside a project.
