---
name: searchdock-setup
description: Set up SearchDock CLI and read-only Google Search Console authentication, choose an account profile and verified property, and check the connection. Use for first installation or reconnecting Google access.
---

Check `node --version` (22 or later) and `searchdock --version`. Reuse a working installation. Otherwise run `npm install --global searchdock-cli`; a no-global alternative is `npx --yes searchdock-cli@0.1.3 <command>`. Python users can run `pipx install searchdock-cli`, but still need Node.js 22+ and Python 3.10+. For a checkout use `npm ci`, `npm run build` and `node dist/cli.cjs`. Verify with `--version` and `doctor --json` before starting Google login.

Install both standalone skills for the current agent, unless a plugin already supplies them:

```sh
npx --yes skills add xplormityai/searchdock-cli --skill searchdock-setup searchdock --agent codex --copy --yes
```

Replace `codex` with the current agent's identifier. Default to project scope; use `--global` only when requested. Without the skills CLI, copy the two repository skill directories to the agent's supported skills location, checking existing destinations before replacing them.

If MCP is supported, merge a server named `searchdock` with command `npx` and args `["--yes", "searchdock-cli@0.1.3", "mcp"]` into the client's configuration. Preserve existing servers and account settings. On Windows, follow the client's process-launch guidance or use an absolute `node` executable with the installed `cli.cjs` path. A plugin already declares this server. Confirm the five `searchdock_*` tools are listed; authentication is a separate verification.

Check `searchdock auth status --profile <name> --json` before reconnecting. If Google is disconnected, tell the user to enable the Search Console API in their own Google Cloud project, configure the OAuth consent screen, add their account as a test user if the app is in testing, and create a Desktop app OAuth client. They must download the JSON locally. Ask only for its path, never its contents. The complete steps are at https://github.com/xplormityai/searchdock-cli/blob/main/docs/google-setup.md.

When connection is requested, run `searchdock auth login --client-file <path> --profile <name>`. The user must complete Google's read-only browser consent; do not bypass it or expose secrets. If the browser cannot open, explain how the user can complete the local flow.

Run `searchdock auth status --profile <name> --json`, then `searchdock sites list --profile <name> --json`. Use the property the user named if verified; ask which property to use when several exist and no site was specified. Set it using `searchdock sites use <property> --profile <name>`, without changing another profile.

Verify `searchdock analytics --profile <name> --days 28 --json`. Explain Search Console's data delay and that missing query rows do not establish zero demand. Report CLI installation, skill installation, MCP discovery and Google verification separately; do not call setup complete while consent or a client restart is pending.

Profiles are stored in the operating system's per-user SearchDock configuration directory, outside the repo. `SEARCHDOCK_CONFIG_DIR` overrides it. Never print client JSON, tokens or private reports or commit them. `auth logout` removes local credentials; revocation in Google Account permissions is separate. OAuth apps left in Google's testing mode can have short-lived refresh tokens; use the Google setup guide when reconnects are frequent.
