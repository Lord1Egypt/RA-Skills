# Install SeekDB — macOS Homebrew

**Prerequisites:** macOS 15+, 1-core CPU, 2 GB RAM, MySQL client installed.

---

## Step 1 — Check Homebrew

```bash
brew --version
sw_vers -productVersion   # confirm macOS >= 15
```
If Homebrew is not installed, tell the user to install it first from <https://brew.sh>, then wait for confirmation before continuing.
If macOS version is below 15, warn the user that it is not officially supported.

## Step 2 — Tap the OceanBase repository

```bash
brew tap oceanbase/seekdb
```
Check for errors. If the tap fails due to network issues, suggest mirror configuration (see tip below).

## Step 3 — Install SeekDB

```bash
brew install seekdb
```
Monitor the output. If it fails, diagnose the error message and fix it.

> **Mirror tip (slow network):** If download is slow or times out, add to `~/.zshrc` and re-run:
> ```bash
> export HOMEBREW_API_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/api"
> export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles"
> ```
> Then: `source ~/.zshrc && brew install seekdb`

## Step 4 — Start SeekDB

```bash
seekdb-start
```
Alternative startup options:
- Foreground mode: `seekdb --nodaemon`
- Custom data directory: `seekdb --base-dir=/custom/path`

## Step 5 — Verify the service is running

```bash
seekdb-status
```
The output should show `running`. If not, diagnose and fix before continuing.

## Step 6 — Verify connectivity

```bash
mysql -h 127.0.0.1 -P 2881 -u root -e "SELECT 'SeekDB is running!' AS status;"
```
If `mysql` CLI is not available, suggest: `brew install mysql-client`

## Step 7 — Done

Confirm success and show connection info:
- MySQL port: `127.0.0.1:2881`
- Start: `seekdb-start` / Stop: `seekdb-stop` / Status: `seekdb-status`
- Cleanup (remove data): `seekdb-cleanup`
- Uninstall: `brew uninstall seekdb`
