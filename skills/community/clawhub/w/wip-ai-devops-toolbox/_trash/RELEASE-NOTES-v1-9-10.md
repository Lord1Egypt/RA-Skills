# Release Notes: AI DevOps Toolbox v1.9.10

**Fix: Release notes files on disk always beat --notes flag**

v1.9.9 shipped with a one-liner on the GitHub release instead of the full narrative release notes. The RELEASE-NOTES-v1-9-9.md file was sitting right there on disk, but `--notes="short text"` took priority because the auto-detect only ran when `--notes` was absent.

This is exactly the kind of bug that happens when a rule exists in documentation but not in code. "Write release notes on the branch" is in the Dev Guide. The tool ignored them.

## What changed

### Notes priority is now enforced (highest wins):

1. `--notes-file=path` ... explicit file path (always wins)
2. `RELEASE-NOTES-v{ver}.md` ... in repo root (always wins over `--notes` flag)
3. `ai/dev-updates/YYYY-MM-DD*` ... today's dev update (wins over `--notes` flag if longer)
4. `--notes="text"` ... fallback only. Use for repos without release notes files.

If a RELEASE-NOTES file exists on disk, `--notes` is ignored and a warning is printed:

```
! --notes flag ignored: RELEASE-NOTES-v1-9-10.md takes priority
```

Written notes on disk always take priority over a CLI one-liner. The agent wrote the file. The tool should use it.

## Files changed

```
 tools/wip-release/cli.js | ~40 lines rewritten (notes cascade logic)
```

## Install

```bash
git pull origin main
```

## Attribution

Built by Parker Todd Brooks, Lesa, and Claude Opus 4.6 at WIP.computer.
