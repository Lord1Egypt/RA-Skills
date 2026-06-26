# Publish Pattern

Use this pattern when turning a local wrapper setup into a ClawHub skill.

## Design Rules

- The skill must target a wrapper or remote CLI contract, not bundled OpenClaw internals.
- Do not claim Linux natively supports a macOS-only tool.
- Keep the wrapper path configurable instead of baking in a user-specific home directory.
- Store credentials outside the skill folder.
- Put node ownership in the setup section, for example:
  - `imsg` lives on `M1`
  - `remindctl` lives on `MacBook Pro`

## Recommended Contract

1. Install the wrapper with `mac-node-bridge`.
2. Verify the wrapper path works from the gateway shell.
3. Make the published skill call the wrapper through a configurable path contract such as `OPENCLAW_BIN_DIR` or a documented default.
4. Treat the wrapper as the dependency boundary.

## Good Example

- Skill: `mac-imessage-remote`
- Setup:
  - install wrapper into the default bridge bin dir or a documented override such as `OPENCLAW_BIN_DIR`
  - verify `"$wrapper_dir/imsg" chats --limit 1`
- Runtime:
  - all message operations call `"$wrapper_dir/imsg"`

## Bad Example

- Patch OpenClaw core so Linux says the bundled macOS `imsg` skill is ready
- Store SSH keys or OAuth tokens in the skill directory
- Assume every node has the same privacy permissions or Homebrew packages
- Hardcode `/home/node/.openclaw/bin/...` into a public skill
