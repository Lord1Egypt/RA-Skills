# Install And Run

## One-Step Setup

```bash
node scripts/install_and_run.js
```

This helper script installs the published third-party npm package `superpowers-ai` into this skill's local state directory and then runs the locally installed CLI.

It installs under:

```text
.superpowers/npm
```

It does not perform a global npm install.

It uses the current shell environment, npm configuration, and normal local permissions for that local install.

Expected package provenance:
- npm page: `https://www.npmjs.com/package/superpowers-ai`
- npm publisher: `superpowersai`
- maintainer email: `rohan@getsupers.com`

The helper is pinned to `superpowers-ai` and does not accept an alternate package name.

The login flow asks for:
- email or phone
- verification code

After verification, the package should start the streamer and print a browser control link.

## Install Only

```bash
node scripts/install_and_run.js --install-only
```

## Start Later

```bash
node scripts/install_and_run.js --start
```

## Stop Later

```bash
node scripts/install_and_run.js --stop
```

## Account Helpers

```bash
node scripts/install_and_run.js --whoami
node scripts/install_and_run.js --logout
```
