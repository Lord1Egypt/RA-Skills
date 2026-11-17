---
name: proxmox-mcp-openclaw
description: Install the immutable Proxmox MCP v0.1.1 GitHub Release locally and register it with OpenClaw.
metadata:
  openclaw:
    requires:
      bins:
        - node
        - openclaw
        - tar
      env:
        - PROXMOX_BASE_URL
        - PROXMOX_TOKEN_ID
        - PROXMOX_TOKEN_SECRET
---

# Proxmox MCP for OpenClaw

This skill installs the immutable `v0.1.1` release from GitHub, verifies its published SHA-256 checksum, and registers the local stdio executable with the supported `openclaw mcp add` command. It is not an OpenClaw plugin or npm package.

The release source is [Theorvane/proxmox-mcp](https://github.com/Theorvane/proxmox-mcp) at immutable `main` commit `6bb3d53a1ee20b9e0a8f885846148aeaa58f5520`, release asset path `proxmox-mcp-0.1.1.tar.gz`. Verify any ClawHub listing against this repository and pinned release before using it.

## Install

Choose a new local directory path that does not yet exist. The target itself must not exist (even if empty); there is no option to reuse a nonempty or pre-existing directory. Export credentials only in the shell that runs the installer; do not place them in files.

```sh
export PROXMOX_BASE_URL='https://proxmox.example:8006'
export PROXMOX_TOKEN_ID='user@realm!token-name'
export PROXMOX_TOKEN_SECRET='set-this-in-your-shell'
node skills/proxmox-mcp-openclaw/scripts/install.mjs /absolute/path/to/proxmox-mcp
```

## Dry run

Validate the required environment and a new absolute target path without changing anything:

```sh
node skills/proxmox-mcp-openclaw/scripts/install.mjs --dry-run /absolute/path/to/proxmox-mcp
```

The credential-free plan prints the pinned release version, archive and checksum URLs, plus the absolute executable command and working directory. A dry run does not create directories, download or inspect archives, invoke OpenClaw, or call Proxmox.

The installer fails before downloading or invoking OpenClaw if any credential is missing. It does not print values, write a credential receipt, edit OpenClaw configuration files, call Proxmox APIs, or use `--no-probe`. OpenClaw's ordinary registration probe can occur only after you explicitly run the command with your credentials.

It refuses any existing destination directory, including an empty one. The archive is verified and fully staged beside the destination before the registration preflight; promotion is an atomic rename only after that preflight succeeds. It also refuses an existing `proxmox-mcp` OpenClaw registration; this installer deliberately has no replacement policy, so remove or rename that registration yourself with the supported OpenClaw CLI before retrying.

The registration performed after verification is:

```sh
openclaw mcp add proxmox-mcp --command /absolute/path/to/proxmox-mcp/proxmox-mcp --cwd /absolute/path/to/proxmox-mcp --env PROXMOX_BASE_URL=... --env PROXMOX_TOKEN_ID=... --env PROXMOX_TOKEN_SECRET=...
```
