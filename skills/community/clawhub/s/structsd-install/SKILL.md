---
title: Install structsd from release or source
meta_description: Install structsd from a prebuilt release binary or build from source with the Makefile. Go 1.23+, no Ignite dependency for builds.
name: structsd-install
description: Installs the structsd binary. Covers downloading prebuilt release binaries (recommended) and building from source via the Makefile (Go 1.23+). Use when structsd is not found, when setting up a new machine, or when the agent needs to install or update the Structs chain binary.
level: entry
domain: infra
---

# Install structsd from release or source

There are two supported paths for installing `structsd`:

1. **Prebuilt release binary** (fastest; no Go toolchain needed)
2. **Build from source via the Makefile** (required for unreleased branches or local patches)

After either path, `structsd` will be available on your PATH and `structsd version` will print the chain version.

> The Makefile builds `structsd` via plain `go build`, so no Ignite CLI is needed for installation. Ignite is only used to run a local devnet via `make serve`.

---

## Path A: Prebuilt Release Binary (recommended)

The chain ships signed binaries via GoReleaser on every tag. Pick the asset for your OS/arch from the latest release at <https://github.com/playstructs/structsd/releases>.

```bash
# Pick one (replace VERSION with e.g. v0.19.1):
VERSION=v0.19.1

# Linux amd64
curl -L -o structsd.tar.gz \
  "https://github.com/playstructs/structsd/releases/download/${VERSION}/structsd_$(echo ${VERSION#v})_linux_amd64.tar.gz"

# macOS Apple Silicon
curl -L -o structsd.tar.gz \
  "https://github.com/playstructs/structsd/releases/download/${VERSION}/structsd_$(echo ${VERSION#v})_darwin_arm64.tar.gz"

tar -xzf structsd.tar.gz
sudo install -m 0755 structsd /usr/local/bin/structsd
rm structsd.tar.gz structsd
```

Verify:

```bash
structsd version
```

If asset names differ on the release page (GoReleaser layouts evolve), copy the URL directly from the release rather than relying on the template above.

---

## Path B: Build from Source (Makefile)

Use this when you need a branch that has not been tagged yet, or when you are developing the chain locally.

### 1. Install Go (1.23+)

The Makefile enforces `REQUIRE_GO_VERSION = 1.23`. Newer minor versions (1.24, 1.25) are also fine.

#### Linux (amd64)

```bash
GO_VER=1.23.6
wget https://go.dev/dl/go${GO_VER}.linux-amd64.tar.gz
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go${GO_VER}.linux-amd64.tar.gz
rm go${GO_VER}.linux-amd64.tar.gz
```

If an older Go was installed via apt, remove it first: `sudo apt remove -y golang-go`

#### macOS (Apple Silicon)

```bash
GO_VER=1.23.6
curl -OL https://go.dev/dl/go${GO_VER}.darwin-arm64.tar.gz
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go${GO_VER}.darwin-arm64.tar.gz
rm go${GO_VER}.darwin-arm64.tar.gz
```

#### macOS (Intel)

```bash
GO_VER=1.23.6
curl -OL https://go.dev/dl/go${GO_VER}.darwin-amd64.tar.gz
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go${GO_VER}.darwin-amd64.tar.gz
rm go${GO_VER}.darwin-amd64.tar.gz
```

Alternatively on macOS: `brew install go@1.23` (or any newer 1.x).

#### Configure PATH

Add to `~/.profile` (or `~/.zshrc` on macOS):

```bash
export PATH=$PATH:/usr/local/go/bin:~/go/bin
```

Reload: `source ~/.profile` (or `source ~/.zshrc`).

#### Verify

```bash
go version
```

Expected: `go version go1.23.x linux/amd64` (or `darwin/arm64`, etc.). The Makefile will refuse to build with anything older than 1.23.

### 2. Clone and Build

```bash
git clone https://github.com/playstructs/structsd.git
cd structsd

# Most common: install into GOPATH/bin (~/go/bin), which is on your PATH
make install

# Or, build a binary into ./build/ without installing it
make build
```

`make install` runs `go install -mod=readonly ./cmd/structsd`, embedding the version, commit hash, and build tags via ldflags. The resulting binary lands at `~/go/bin/structsd`.

`make build` writes to `./build/structsd` instead.

If you need cross-compiled binaries, the Makefile also exposes `build-linux-amd64`, `build-linux-arm64`, `build-darwin-amd64`, `build-darwin-arm64`, and `build-windows-amd64`, plus `build-all` to do every supported platform in one shot.

#### Verify

```bash
structsd version
```

### 3. Update structsd

```bash
cd structsd
git fetch --tags
git checkout v0.19.1   # or `git pull origin main` for tip-of-tree
make install
```

`make install` is idempotent -- it overwrites the previous binary at `~/go/bin/structsd`.

---

## Optional: Local Devnet (Ignite)

Only required if you want to run a chain locally for development.

```bash
# One-time
curl https://get.ignite.com/cli! | bash
ignite version

# In the structsd repo:
make serve              # ignite chain serve
make serve-reset        # ignite chain serve --reset-once
make serve-reset-verbose
```

For mainnet/testnet client use, you do **not** need Ignite -- a `structsd` binary from Path A or Path B is sufficient.

---

## Quick Check

Run all verifications in sequence:

```bash
go version && structsd version
```

If you also installed Ignite for local serving:

```bash
go version && ignite version && structsd version
```

If any command fails, revisit the corresponding step above.

## Troubleshooting

- **`structsd: command not found`** — Ensure `~/go/bin` (Path B) or `/usr/local/bin` (Path A) is on your PATH. Run `command -v structsd` to confirm.
- **`go: command not found`** — Ensure `/usr/local/go/bin` is on your PATH. Reload your shell profile.
- **`ERROR: Go version 1.23+ is required`** from `make install` — Your Go is too old. Re-install per step 1 above; the Makefile's `check_version` target enforces this hard.
- **Build fails on `go mod tidy`** — Network access is required for the first build. Retry once you have connectivity, or set `GOPROXY=direct` if you are behind a restrictive proxy.
- **Permission denied on `/usr/local`** — Use `sudo` for the tar extraction or for `install -m 0755`. On shared systems, ask your administrator. Path B does not require root because it installs to `~/go/bin`.
- **`gcc not installed for ledger support`** — Either install `gcc` (`sudo apt install build-essential` / `xcode-select --install`) or build with `LEDGER_ENABLED=false make install`.

## See Also

- [TOOLS](https://structs.ai/TOOLS) — Environment configuration (servers, account, after structsd is installed)
- [structs-onboarding skill](https://structs.ai/skills/structs-onboarding/SKILL) — Player creation and first builds (requires structsd)
- [structs-desktop](https://github.com/playstructs/structs-desktop) — Desktop app for human players; embeds the MCP server agents connect to (see [TOOLS](https://structs.ai/TOOLS))
- [structsd releases](https://github.com/playstructs/structsd/releases) — Prebuilt binaries per OS/arch and changelog per tag
