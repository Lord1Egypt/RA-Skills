###### WIP Computer

# License Guard

Enforce licensing on every repo. Copyright, dual-license, CLA, README license section. Checked automatically on every release.

## Commands

```bash
wip-license-guard check                  # audit current repo
wip-license-guard check --fix            # audit and auto-fix issues
wip-license-guard init                   # interactive first-run setup
wip-license-guard init --from-standard   # apply WIP Computer defaults without prompting
wip-license-guard readme-license         # audit license blocks across all repos
wip-license-guard readme-license --fix   # apply standard license block to all READMEs
wip-license-guard readme-license --dry-run  # preview changes without writing
```

## What it checks

- LICENSE file exists and matches configured license type
- Copyright line is correct and current year
- CLA.md exists (if configured)
- README has a `## License` section with the standard block
- For toolbox repos: checks every sub-tool in `tools/`

## Config

`.license-guard.json` in repo root. Created by `init`. Contains copyright holder, license type, year, and what to enforce.

```json
{
  "copyright": "WIP Computer, Inc.",
  "license": "MIT+AGPL",
  "year": 2026,
  "enforceCLA": true,
  "enforceReadmeLicense": true
}
```

## wip-release gate

Step 0 of wip-release reads `.license-guard.json` and runs the same checks. If compliance fails, the release is blocked.

## `--from-standard` generates

- `.license-guard.json` with WIP Computer defaults
- `LICENSE` file (dual MIT+AGPL)
- `CLA.md`

## readme-license

Scans all repos in a directory and applies a standard license block to every README. Removes duplicate license sections from sub-tool READMEs. Reads templates from `ai/wip-templates/readme/`.

## Source

Pure JavaScript, no build step. Zero dependencies.

- `cli.mjs` ... CLI entry point
- `core.mjs` ... license checking and generation logic
- `hook.mjs` ... wip-release gate integration

## Interfaces

- **CLI**: `wip-license-guard`

## Part of [AI DevOps Toolbox](https://github.com/wipcomputer/wip-ai-devops-toolbox)

Built by Parker Todd Brooks, Lēsa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).
