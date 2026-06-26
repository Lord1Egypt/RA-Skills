---
name: core-installation
description: Installing pnpm via standalone script, Corepack, npm, or system package managers
---

# Installation

How to install pnpm on a system.

## Prerequisites

Node.js v18.12+ is required unless using standalone script or `@pnpm/exe`.

## Standalone Script

Install without Node.js:

```sh
# POSIX (macOS, Linux)
curl -fsSL https://get.pnpm.io/install.sh | sh -

# Or with wget
wget -qO- https://get.pnpm.io/install.sh | sh -
```

```powershell
# Windows (PowerShell) - may be blocked by Defender; prefer npm/corepack
Invoke-WebRequest https://get.pnpm.io/install.ps1 -UseBasicParsing | Invoke-Expression
```

Install specific version:
```sh
curl -fsSL https://get.pnpm.io/install.sh | env PNPM_VERSION=9.0.0 sh -
```

## Corepack (Recommended with Node.js)

Node.js 16.13+ ships Corepack. Enable pnpm:

```sh
corepack enable pnpm
```

Pin project to specific pnpm version (adds `packageManager` to package.json):

```sh
corepack use pnpm@latest-10
```

## npm

```sh
npm install -g pnpm@latest-10
```

Or use `@pnpm/exe` (bundled with Node.js, works without Node installed):

```sh
npx pnpm@latest-10 dlx @pnpm/exe@latest-10 setup
```

## System Package Managers

```sh
# Homebrew
brew install pnpm

# winget (Windows)
winget install -e --id pnpm.pnpm

# Scoop
scoop install nodejs-lts pnpm

# Chocolatey
choco install pnpm

# Volta
volta install pnpm
```

## Compatibility

| Node.js | pnpm 8 | pnpm 9 | pnpm 10 |
|---------|--------|--------|---------|
| 16      | ✔️     | ❌     | ❌      |
| 18      | ✔️     | ✔️     | ✔️      |
| 20, 22, 24 | ✔️  | ✔️     | ✔️      |

## Key Commands

```bash
pnpm self-update   # Update pnpm
```

## Windows Defender

If installs are slow on Windows, exclude store from Defender:

```powershell
Add-MpPreference -ExclusionPath $(pnpm store path)
```

## Key Points

- Prefer **Corepack** when using Node.js for version pinning
- Use **standalone script** when Node.js is not installed
- `corepack use pnpm@X` pins version per project via `packageManager` field
- For CI, see continuous-integration docs

<!--
Source references:
- https://pnpm.io/installation
-->
