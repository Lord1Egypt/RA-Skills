# Bug: Global `crystal` runs from private repo via npm link

**Filed by:** CC Mini (cc-mini) on 2026-03-13
**Severity:** High. Production tool runs from development source.

## What's wrong

The global `crystal` binary is npm-linked to the private repo clone:

```
/opt/homebrew/bin/crystal
  -> /opt/homebrew/lib/node_modules/memory-crystal/dist/cli.js
    -> symlink to repos/ldm-os/components/memory-crystal-private/
```

This was set up via `npm link` on 2026-03-03. It violates the "never run tools from repo clones" rule.

### Consequences

1. Any `git pull`, version bump, or code change in the repo instantly changes the production tool
2. Bumping package.json to v0.7.7 during `wip-release` silently updated the global binary
3. If someone runs `npm install` or `npm run build` in the repo, the production tool changes mid-session
4. Lesa's OpenClaw extension chains through: `~/.openclaw/extensions/memory-crystal/` -> `~/.ldm/extensions/memory-crystal/` -> (copied dist files that match the repo). The OpenClaw path is correct (symlink to LDM), but the LDM extension dist files are identical to the repo's dist, meaning they were likely copied from the repo recently

### Current state (audited 2026-03-13)

| Location | Type | Version | Points to |
|----------|------|---------|-----------|
| `/opt/homebrew/bin/crystal` | symlink | v0.7.7 | repo clone (via npm link) |
| `~/.ldm/extensions/memory-crystal/` | real dir | v0.7.7 | copied files (dist identical to repo) |
| `~/.openclaw/extensions/memory-crystal/` | symlink | v0.7.7 | `~/.ldm/extensions/memory-crystal/` |
| Repo `package.json` | source | v0.7.7 | n/a |

## Fix plan

### Step 1: Unlink the global binary

```bash
cd "/Users/lesa/Documents/wipcomputer--mac-mini-01/staff/Parker/Claude Code - Mini/repos/ldm-os/components/memory-crystal-private"
npm unlink -g
```

This removes the symlink from `/opt/homebrew/lib/node_modules/memory-crystal/`.

### Step 2: Install from npm registry

```bash
npm install -g memory-crystal@0.7.7
```

This installs the published package (not the repo). The global `crystal` now runs from a frozen copy of the published version.

### Step 3: Verify the LDM extension is independent

Check if `~/.ldm/extensions/memory-crystal/dist/` files are symlinks or real copies:

```bash
file ~/.ldm/extensions/memory-crystal/dist/cli.js
ls -la ~/.ldm/extensions/memory-crystal/dist/cli.js
```

If they're real files (not symlinks), the LDM extension is already independent. If any are symlinks to the repo, copy them to break the link.

### Step 4: Verify separation

After fix, confirm nothing points to the repo:

```bash
# Global should NOT be a symlink to the repo
ls -la /opt/homebrew/lib/node_modules/memory-crystal

# LDM extension should be independent
diff -q ~/.ldm/extensions/memory-crystal/dist/cli.js \
  "/path/to/repo/dist/cli.js"
# Files may be identical in content but should be separate copies
```

### Step 5: Prevent recurrence

Add a check to `crystal doctor` that warns if the global binary is npm-linked instead of npm-installed. Something like:

```bash
readlink /opt/homebrew/lib/node_modules/memory-crystal
# If this returns a path, it's linked. Warn the user.
```

Also add this to the Dev Guide: "Never use `npm link` for tools that are also installed globally. Use `npm install -g` from the registry."

## What NOT to do

- Don't just re-run `crystal init`. It may re-create the link.
- Don't delete anything. Unlink, then install cleanly.
- Don't touch `~/.openclaw/extensions/memory-crystal/`. That symlink to LDM is correct per the Dev Guide.
