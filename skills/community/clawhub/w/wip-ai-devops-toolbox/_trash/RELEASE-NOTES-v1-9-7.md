# Release Notes: AI DevOps Toolbox v1.9.7

## LDM OS Integration

AI DevOps Toolbox now works with LDM OS when it's available.

### wip-install delegates to ldm install

When the `ldm` CLI exists on PATH, `wip-install` delegates to `ldm install`. LDM OS handles the scaffold, interface detection, and extension deployment. The Toolbox's standalone behavior is preserved as a fallback when `ldm` isn't available.

Supports `--dry-run` and `--json` passthrough to `ldm install`.

### LDM OS tip

After standalone installs, the Toolbox prints a tip: "Run `ldm install` to see more skills you can add."

### Universal Installer link

The "Read more about Universal Installer" link now points to the LDM OS docs page. The Universal Installer engine moved to LDM OS. The Toolbox keeps `wip-install` as an entry point that delegates.

### Part of LDM OS

README includes a "Part of LDM OS" section linking back to the LDM OS repo.
