# Release Notes: wip-ldm-os v0.4.64

Closes #249

## Installer deploys bridge on CLI update

The bridge MCP server (lesa-bridge) lives inside the LDM OS npm package but deploys to `~/.ldm/extensions/lesa-bridge/dist/`. When `ldm install` updated the CLI, it did the `npm install -g` but never copied the bridge files to the extension directory. Bridge fixes shipped in v0.4.63 (the model param fix) didn't take effect until someone manually copied the files.

Now `ldm install` deploys bridge files automatically on both CLI update and init. It compares the npm package version against the deployed version and copies only when they differ.
