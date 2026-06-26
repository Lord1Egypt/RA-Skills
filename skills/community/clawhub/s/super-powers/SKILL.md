---
name: superpowers-streamer-cli
description: Install and run the published SuperPowers desktop streamer npm package. Use when a user needs a portable ClawHub skill that installs the third-party npm package `superpowers-ai`, executes its CLI in the user's current environment, logs in or creates an account with email or phone verification, starts the streamer, opens the printed control link, and helps recover from common npm or runtime issues without requiring source-code access.
metadata:
  clawdbot:
    config:
      requiredEnv: []
      stateDirs: [".superpowers"]
      example: "config = { };"
    cliHelp: |
      node scripts/install_and_run.js --help
      node scripts/install_and_run.js
      node scripts/install_and_run.js --start
      node scripts/install_and_run.js --stop
---
# SuperPowers Streamer CLI

Use this skill when the user only needs the published npm package workflow.

Assume:
- no source-code access
- no repo edits
- the package can be installed in any normal npm environment

## Important Behavior

This skill's helper script does not build local source code.

It will:
- install the published third-party npm package `superpowers-ai` into the skill's local `.superpowers/npm` directory
- execute the locally installed CLI from that isolated state directory
- do that using the user's current npm config and normal local permissions

It does not perform a global npm install.

Use this skill only when that package-install-and-run behavior is what the user wants.

## Package Provenance

The helper is designed around this published package:

- npm package: `superpowers-ai`
- npm page: `https://www.npmjs.com/package/superpowers-ai`
- expected npm publisher: `superpowersai`
- expected maintainer email: `rohan@getsupers.com`

When explaining this skill, be explicit that it installs and executes that published npm package on the user's machine.

The helper is intentionally pinned to that one package. It does not accept an alternate npm package name.

## Main Flow

1. Confirm `node` and `npm` exist.
2. Install `superpowers-ai` into `.superpowers/npm`.
3. Run the login or create-account flow.
4. Let the package auto-start the streamer after verification.
5. If needed, start it again manually and open the printed `/general` control link.

## Fastest Path

Run:

```bash
node scripts/install_and_run.js
```

That script:
- installs the published third-party npm package `superpowers-ai` into `.superpowers/npm`
- retries with a temp npm cache if the normal install fails
- runs the locally installed CLI from the skill state directory
- runs the package's login flow by default

## Other Modes

Install only:

```bash
node scripts/install_and_run.js --install-only
```

Start only:

```bash
node scripts/install_and_run.js --start
```

Stop the local streamer:

```bash
node scripts/install_and_run.js --stop
```

Show the saved account:

```bash
node scripts/install_and_run.js --whoami
```

Log out:

```bash
node scripts/install_and_run.js --logout
```

## Customer Commands

Through this skill helper, the main commands are:

```bash
node scripts/install_and_run.js
node scripts/install_and_run.js --start
node scripts/install_and_run.js --stop
node scripts/install_and_run.js --whoami
node scripts/install_and_run.js --logout
```

## macOS Notes

On macOS, the user may need to allow:
- Screen Recording
- Accessibility

If macOS prompts for permissions, approve them and rerun:

```bash
node scripts/install_and_run.js --start
```

## Troubleshooting

Read `references/install.md` for install and usage wording.
Read `references/troubleshooting.md` for common npm, login, and streaming failures.
