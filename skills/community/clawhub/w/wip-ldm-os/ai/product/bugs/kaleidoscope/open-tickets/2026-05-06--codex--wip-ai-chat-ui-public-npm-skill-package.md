# WIP AI Chat UI skill: public npm package from private source

Status: Open
Priority: P1
Owner: Coder
Area: Kaleidoscope, LDM OS installer, WIP design skills

## Problem

The WIP AI Chat UI guidance is useful across Kaleidoscope, Remote Control, and future WIP chat surfaces, but it is currently living as repo-local design skill material instead of a durable installer-distributed skill.

The product decision is:

- Source can live in a private WIP working repo.
- The npm tarball should be public.
- LDM OS should install the skill as a normal package.
- Symlink install is not the product path.
- Manual copy scripts are not the product path.
- This is not a React component library.
- This must not add assistant-ui runtime dependencies.

## Canonical Source Path

Confirm the literal repo path before editing. The expected source path is:

```text
/Users/lesa/wipcomputerinc/repos/wip-inc/design/skills/wip-ai-chat-ui/
```

If the local repo has been renamed to `wip-inc-private-only`, use the literal disk path. Do not treat `wip-inc` as a logical alias in commands.

The canonical skill folder should be:

```text
design/skills/wip-ai-chat-ui/
```

Do not use nested private folder names such as:

```text
design/wip-design-private/
design/wip-inc-private-only/
```

Repo privacy belongs at the repo boundary, not inside the `design/` folder.

## Package Name

Use the scoped public npm package:

```text
@wipcomputer/wip-ai-chat-ui
```

`package.json` must include:

```json
{
  "name": "@wipcomputer/wip-ai-chat-ui",
  "license": "MIT",
  "publishConfig": {
    "access": "public"
  }
}
```

Scoped npm packages default to private unless `publishConfig.access` or `npm publish --access public` is used. Prefer `publishConfig.access` so the release cannot forget it.

## Required Fixes

1. Normalize the source folder:
   - canonical path is `design/skills/wip-ai-chat-ui/`
   - no nested `design/wip-design-private/`
   - duplicate or old copies can move under `design/skills/_trash/`

2. Fix broken references:
   - `SKILL.md` references four files under `references/`
   - `stack.md` and `anti-patterns.md` already exist in the live tree
   - restore the missing files from `_trash/wip-ai-chat-ui-01/` if needed:
     - `references/components.md`
     - `references/remote-control.md`

3. Add `design/README.md`:
   - design skills live under `design/skills/<name>/`
   - install through LDM OS
   - no nested private or private-only naming inside `design/`
   - repo privacy is handled at the repo boundary

4. Add public npm package shape:
   - `package.json`
   - `README.md`
   - `LICENSE`
   - `test/release-shape.test.mjs`

5. Add package metadata:
   - `description`
   - `repository`
   - `bugs`
   - `keywords`
   - `license`
   - `publishConfig.access`
   - `files` whitelist

6. Add lifecycle scripts:

```json
{
  "scripts": {
    "test": "node test/release-shape.test.mjs",
    "prepack": "node test/release-shape.test.mjs",
    "prepublishOnly": "npm test"
  }
}
```

The release-shape test must block bad package contents before pack or publish.

## Release Shape Contract

Use a `files` whitelist in `package.json`. Do not rely on `.npmignore` as the primary protection.

The release-shape test must verify the packed tarball excludes:

- `ai/`
- `_trash/`
- `_sort/`
- `.env`
- `.worktrees/`
- `node_modules/`

The release-shape test must verify the packed tarball includes:

- `SKILL.md` or the package's exported skill path
- `references/stack.md`
- `references/components.md`
- `references/anti-patterns.md`
- `references/remote-control.md`
- `README.md`
- `LICENSE`
- `package.json`

All four `references/*.md` files referenced from `SKILL.md` must resolve to files that ship in the tarball.

## Installer Contract

LDM OS should install the skill through the package path, not through a manual symlink.

Expected product path:

```text
ldm install @wipcomputer/wip-ai-chat-ui
```

If local-path dry run is needed during development, use the literal source path and confirm what the installer detects before writing files.

The installer documentation should point to:

```text
source path: design/skills/wip-ai-chat-ui/
package: @wipcomputer/wip-ai-chat-ui
install path: ldm install
```

## Hard Boundaries

- Do not make this a shared React component package.
- Do not install `@assistant-ui/react`.
- Do not install `@assistant-ui/ui`.
- Do not adopt Assistant Cloud.
- Do not add Vercel AI SDK provider routing.
- Do not change Remote Control, Kaleidoscope, relay, daemon, auth, persistence, or protocol as part of this package work.
- Do not ship `_trash/`, planning files, or private workspace files in npm.

## Acceptance

- Canonical source path is clear and matches the actual disk path.
- `design/skills/wip-ai-chat-ui/` is the only live skill source.
- Duplicate copies are removed from the live skill path or moved under `_trash/`.
- `SKILL.md` has no broken links to reference files.
- `npm test` passes.
- `npm pack --dry-run` or equivalent release-shape validation passes.
- Tarball contains only public skill files.
- Tarball includes all four referenced docs.
- Tarball excludes `_trash/`, `ai/`, `_sort/`, `.env`, `.worktrees/`, and `node_modules/`.
- `publishConfig.access` is public.
- No assistant-ui runtime dependency is added.
- LDM OS installer docs or tickets point to the final canonical path and package name.

## Notes

This ticket captures the packaging and installer decision only. It does not authorize Kaleidoscope UI implementation work.
