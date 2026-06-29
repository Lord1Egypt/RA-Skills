# Third-Party Notices

XDesign v1.x ships with code, themes, templates, and assets from the following
upstream projects. Each is included under its original license; the full
license texts are preserved in their respective directories.

| Component | Upstream | License | Location in this repo |
|---|---|---|---|
| **HTML PPT Studio** (deck-studio/) | [lewislulu/html-ppt-skill](https://github.com/lewislulu/html-ppt-skill) © 2026 lewis | MIT | [`deck-studio/LICENSE`](./deck-studio/LICENSE) |

## What this means in practice

The `deck-studio/` subdirectory is a snapshot clone of the upstream
`html-ppt-skill` repository. The original MIT license (which requires
preservation of the copyright notice and permission notice) is retained
verbatim in `deck-studio/LICENSE`. No source files in `deck-studio/` were
modified beyond:

1. Renaming `deck-studio/SKILL.md` → `deck-studio/SUBMODULE.md` so that
   XDesign has a single skill entry point (the parent `SKILL.md`).
2. Substituting the 18 themes actually present in this snapshot
   (the upstream advertises 36 themes; we cloned a curated subset).
3. Prepending a one-paragraph note to `SUBMODULE.md` pointing agents
   back to the parent `SKILL.md` for routing decisions.

All other files in `deck-studio/` are byte-identical to the upstream
snapshot at the time of integration. To re-sync with upstream, follow
the procedure in [`references/integration-guide.md`](./references/integration-guide.md#upstream-sync-procedure).

## Trademarks

"XDesign" and the XDesign mark are property of the XDesign authors.
"HTML PPT Studio" and any associated marks are property of the
html-ppt-skill authors. Use of either mark in derived works should
follow fair-use principles and the underlying license terms.
