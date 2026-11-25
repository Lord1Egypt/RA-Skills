# Antigravity CLI

In this version the Antigravity CLI runs the attendant **in session, in assisted mode only**. It has no unattended runner yet: the CLI has no per-run way to restrict the tools of a customer's process, so an unattended customer turn could not be made safe.

## Install and keep it current

```
agy plugin install https://github.com/turbo-notify/agent-skills
```

Run the same command again to update (it replaces the installed copy). Antigravity installs from GitHub without a version tag, so it follows the latest stable version. Each cycle checks the version and tells the administrators when a new one exists.

## Connect Turbo Notify

The plugin already declares the server (`mcp_config.json`), so `agy plugin list` shows it as a component after the install. Sign in under Agent settings, Customizations, Authenticate next to the server, and paste the code back. To use an API key instead, or without the plugin: `agy mcp add turbo-notify https://mcp.turbonotify.com`, passing the key as a header with `-H "Authorization: Bearer …"`.

## Run

Follow [tick.md](tick.md) and [contact-turn.md](contact-turn.md) in a session you keep open, one customer at a time, always in assisted mode (a person approves each draft). Tell the person who set it up that the attendant stops when the session closes.

## What it cannot do

No unattended mode, no fresh context per customer. If the business needs answers around the clock, use Claude Code or Codex for the runner.
