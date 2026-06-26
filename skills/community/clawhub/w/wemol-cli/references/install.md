# Install

Use the installer scripts when `wemol-cli` is not already available, or when installed version is below the required skill baseline.

Agent workflow:
- First check whether `wemol-cli` is installed and read its version:

```bash
wemol-cli --version
```

- Required baseline for this skill: `v1.0.0`.
- If the command is missing, continue with the installer commands below.
- If installed version is `< v1.0.0`, run the installer commands below to upgrade.
- If installed version is `>= v1.0.0`, do not reinstall unless the user explicitly asks for upgrade/reinstall.
- After installation, run `wemol-cli --help` again to verify the installation.

Version comparison examples:

```bash
required="1.0.0"
current="$(wemol-cli --version | awk '{print $2}' | sed 's/^v//')"
if [ "$(printf '%s\n' "$required" "$current" | sort -V | head -n1)" != "$required" ]; then
  echo "upgrade needed"
fi
```

```powershell
$required = [Version]"1.0.0"
$currentRaw = (wemol-cli --version).Split()[1].TrimStart("v")
$current = [Version]$currentRaw
if ($current -lt $required) { "upgrade needed" }
```

## macOS and Linux

Install with the Unix installer:

```bash
curl -LsSf https://wemol.wecomput.com/static/wemol-cli/latest/install.sh | sh
```

The default release base URL is:

```text
https://wemol.wecomput.com/static/wemol-cli
```

To override it temporarily:

```bash
curl -LsSf https://wemol.wecomput.com/static/wemol-cli/latest/install.sh | \
  WEMOL_INSTALL_BASE_URL="https://your-release-base" sh
```

To install a specific version:

```bash
curl -LsSf https://wemol.wecomput.com/static/wemol-cli/latest/install.sh | \
  sh -s -- --version v1.0.0
```

Agent notes:
- Use the `latest/install.sh` URL above, not a versioned installer path.
- When `--version` is omitted, the installer treats `latest` as a release directory alias. It downloads `latest/SHA256SUMS` from the release base URL and selects the matching artifact for the current platform.
- If a specific version is given without the `v` prefix, the installer adds it automatically.
- The installer checks whether `~/.wemol/bin` is already on `PATH` and prints the shell snippet to add it when needed.

The installer places the binary in:

```bash
~/.wemol/bin/wemol-cli
```

If `wemol-cli` is not on `PATH`, the installer prints the shell snippet needed to add it.

## macOS Security Notice

Current macOS builds are not yet distributed with a valid developer signature/notarization chain.

On a new Mac, the first launch may be blocked by Gatekeeper. If that happens, ask the user to manually allow the binary:

1. Try running `wemol-cli --help` once.
2. Open `System Settings -> Privacy & Security`.
3. Find the blocked `wemol-cli` item and choose `Allow Anyway`.
4. Run the command again and confirm the security prompt.

This is currently expected for macOS release builds until official signing is added.

## Windows

Install with the PowerShell installer:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://wemol.wecomput.com/static/wemol-cli/latest/install.ps1 | iex"
```

To override the release base URL:

```powershell
$env:WEMOL_INSTALL_BASE_URL = "https://your-release-base"
powershell -ExecutionPolicy ByPass -c "irm https://wemol.wecomput.com/static/wemol-cli/latest/install.ps1 | iex"
```

To install a specific version:

```powershell
powershell -ExecutionPolicy ByPass -c "& ([scriptblock]::Create((irm https://wemol.wecomput.com/static/wemol-cli/latest/install.ps1))) -Version v1.0.0"
```

Agent notes:
- Use the `latest/install.ps1` URL above, not a versioned installer path.
- When `-Version` is omitted, the installer treats `latest` as a release directory alias. It downloads `latest/SHA256SUMS` from the release base URL and selects the matching artifact for the current platform.
- If a specific version is given without the `v` prefix, the installer adds it automatically.
- The installer checks whether `$HOME\.wemol\bin` is already in the user `Path` and prints a reminder when it is missing.

The installer places the binary in:

```powershell
$HOME\.wemol\bin\wemol-cli.exe
```

## Windows Security Notice

Current Windows builds are not yet distributed with a code-signing certificate.

Because of that, Windows Defender SmartScreen or browser download protection may warn about `wemol-cli.exe` on first download or launch. If that happens, ask the user to review the file source and then use the standard Windows override flow, such as:

1. Keep the downloaded file if the browser marks it as uncommon.
2. Run `wemol-cli.exe --help` once.
3. If SmartScreen blocks it, choose `More info` and then `Run anyway`.

This is currently expected for Windows release builds until official code signing is added.

## Verification

After installation, verify:

```bash
wemol-cli --help
```

If the command is still missing, check the install directory and `PATH`.

## Update-Question Workflow (Mandatory)

When user asks whether `wemol-cli` needs an update, execute this workflow and provide a direct conclusion.

1. Check installed version:

```bash
wemol-cli --version
```

2. Determine local baseline (this skill baseline is `v1.0.0`; if working inside this repo, also read `crates/cli/Cargo.toml` version as local source-of-truth).

3. Decision rules:
- If installed `< v1.0.0`: conclude **update required**.
- If installed `< repo CLI version` (when repo version is available): conclude **update required**.
- If installed `== repo CLI version` (or `>= v1.0.0` and no higher trusted source found): conclude **no mandatory update from local evidence**.

4. Upstream latest check:
- If network/channel access is available, attempt upstream check directly (official release page or configured distribution channel).
- If upstream check is blocked (network/channel unavailable), explicitly report what was checked and what is blocked.

Required response style:
- Do not ask the user to perform the comparison themselves as the primary answer.
- Return one of: `update required`, `no update required from current evidence`, or `cannot verify upstream latest due to <specific blocker>`.
