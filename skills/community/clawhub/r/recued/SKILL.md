---
name: recued
description: Work with your own Recued server from OpenClaw. Read your notes, tasks and the things you own, and propose changes that wait for your approval in Recued.
homepage: https://recued.com
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["RECUED_MCP_TOKEN"] },
        "primaryEnv": "RECUED_MCP_TOKEN",
        "envVars":
          [
            {
              "name": "RECUED_MCP_TOKEN",
              "required": true,
              "description": "The key of a contract you make for OpenClaw in the Recued web app. OpenClaw gets only the tools that contract grants.",
            },
          ],
        "homepage": "https://recued.com",
      },
  }
---

# Recued

Recued is a server you run on a computer you control. It keeps your notes, tasks, mail, calendar
and the things you own, and it stands between your data and any AI. An AI app reads and acts
through Recued: Recued checks every request against what you granted, asks you before a change,
and keeps a record of what was done.

This skill connects OpenClaw to your Recued server and tells OpenClaw how to work with it. It
installs nothing and runs no commands.

## Set it up

1. Install Recued on a computer you control: https://recued.com/docs/setup/install-server/
   Read the installer before you run it. It checks the release's signature before it installs
   anything.
2. In the Recued web app, open Contracts and make a contract for OpenClaw. Choose the tools it may
   use, and copy the contract's key when Recued shows it.
3. Put the key where OpenClaw's gateway can read it, in `~/.openclaw/.env`:

   ```
   RECUED_MCP_TOKEN=<the contract's key>
   ```

4. Add the server. On the computer Recued runs on, its address is `http://127.0.0.1:7717/mcp`.
   From another computer, use the address the contract's Connect tab shows.

   ```
   openclaw mcp set recued '{"url":"http://127.0.0.1:7717/mcp","transport":"streamable-http","headers":{"Authorization":"Bearer ${RECUED_MCP_TOKEN}"}}'
   ```

   Keep the single quotes, so `${RECUED_MCP_TOKEN}` stays in the config as a placeholder and the
   key itself stays in `~/.openclaw/.env`.

5. Restart the gateway with `openclaw daemon restart`, then run `openclaw mcp probe recued`. It
   lists the tools the contract grants.

## Working with Recued

- Recued's tools appear as `recued__<name>`, with dots turned into dashes: `work.create` is
  `recued__work-create`.
- Look at a tool's arguments before you first call it. A note's text goes in `body`, for example.
- Reading runs at once: searching and reading the user's notes, tasks and the things they own.
- A change waits for the user. When a tool answers `awaiting_approval` with an `action_ref`, the
  change is queued, and that is success, not an error. Tell the user it needs their approval in
  the Recued app, from the bell at the top of the page. Do not send the change again.
- Do not keep checking while you wait. When the user says they have answered, call
  `recued_actionStatus` once with the `action_ref` and report what it says. Do not say a change
  is done before that.
- If Recued refuses a tool, OpenClaw's contract does not grant it. Tell the user which tool, so
  they can decide in the Recued web app whether OpenClaw should have it.

## Privacy

The user's data stays on their Recued server. OpenClaw's model sees only what a tool returns,
and Recued gives OpenClaw only what its contract grants.
