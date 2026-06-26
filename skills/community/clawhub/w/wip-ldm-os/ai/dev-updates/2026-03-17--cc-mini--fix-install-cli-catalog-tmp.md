# Fix ldm install: CLIs, catalog fallback, /tmp/ symlinks, help

Five interconnected bugs fixed in ldm install:

1. **Global CLIs not updated (#81):** Added a second loop in `cmdInstallCatalog()` that checks `state.cliBinaries` against catalog `cliMatches`. CLIs installed via `npm install -g` are now detected and updated.

2. **Catalog fallback (#82):** When no catalog entry matches an extension, falls back to `package.json` `repository.url` instead of skipping. Also added `wip-branch-guard` to catalog registryMatches/cliMatches.

3. **/tmp/ symlink prevention (#32):** `installCLI()` in deploy.mjs now tries the latest npm version before falling back to local `npm install -g .`. This prevents /tmp/ symlinks in most cases.

4. **/tmp/ cleanup (#32):** After `installFromPath()` completes, /tmp/ clones are deleted automatically.

5. **--help flag:** `ldm install --help` now shows usage instead of triggering a real install.

Closes #81, #82. Partial fix for #32.
