# Packaging and changelog reference

## The .skill package format

Claude's settings UI exports and imports skills as `.skill` files. These are
standard ZIP archives containing a directory named after the skill:

```
skill-name.skill (ZIP)
└── skill-name/
    ├── SKILL.md
    ├── MANIFEST.yaml
    ├── CHANGELOG.md
    ├── README.md
    ├── assets/
    └── references/
```

The versioning artifacts travel safely inside the archive. When bootstrapping
or updating a bundle, include them so provenance survives platform round
trips. Some uploaders accept only `.zip` or `.md`; when appropriate, rename
the archive from `.skill` to `.zip` without changing its contents.

Keep the always-loaded `SKILL.md` concise and put detailed reference material
in load-on-demand files. Claude Code exposes `${CLAUDE_SKILL_DIR}` for
bundle-relative paths; other platforms may require paths relative to the
bundle root.

An authored package must include every file listed by its manifest. A reduced
strict-loader or registry package is valid only when its own derived manifest
lists exactly the reduced inventory. Never place a canonical manifest in an
archive that omits manifest-listed files.

## Changelog format

Keep `CHANGELOG.md` at the bundle root beside `SKILL.md` and `MANIFEST.yaml`,
with the newest entry first. If canonical source lives in Git, older history
may be preserved in an append-only repository changelog outside the bundle.

```
# Changelog

## 5.1.0 - 2026-02-10
- SKILL.md: Rewrote layout rules and added a validation checklist.
- evals.json: Not updated; stale until the expectations are aligned.

## 5.0.0 - 2026-02-09
- SKILL.md: Reworked body flow rules and added an optional appendix.
- evals.json: Updated the content-flow expectation.
```

Every entry names every changed file and describes intent. Explicitly identify
dependent files that were not updated and may be stale. Write human-readable
prose rather than a generated diff. Keeping the newest 5 to 15 entries in the
portable bundle is reasonable when the source repository maintains the full
append-only archive.
