---
name: indexion-identity
description: Detect and review name/content drift in code using `indexion identity audit`, then plan verified renames, moves, folder changes, or splits.
---

# Identity Audit Workflow

Use this skill when checking whether function, file, or folder names still match
their contents.

The CLI scans files, folders, and graph-level declaration symbols. It does not
treat every local variable, parameter, or field as an independent naming target;
those can still influence the containing file summary. File names are evaluated
with parent scope, and declaration-heavy files should normally be read as
evidence-thin until follow-up inspection proves an actual rename or split.

## Pipeline

1. Run the mechanical scan:

   ```bash
   indexion identity audit .
   ```

   For a machine-readable queue:

   ```bash
   indexion identity audit --format=json --output=.indexion/cache/identity/report.json .
   ```

2. Treat each row as a review candidate, not proof. Compare:

   - `name`: the scoped name inferred by the identity package
   - `expected_summary`: what the path/name/scope predicts
   - `actual_summary`: graph-derived declarations, docs, module notes, and path terms
   - `assessment`: whether this is actual drift, overbroad content, or insufficient content
   - `recommendation`: first operation to verify

3. Verify before editing:

   ```bash
   indexion doc graph --format=text <path>
   indexion grep --semantic=name:<symbol> .
   rg "<name-or-term>" <path>
   ```

4. Choose the smallest confirmed operation:

   - Treat `insufficient-content` as an evidence problem, not a naming-drift proof.
     Inspect whether the file is intentionally declarative/thin, unsupported by the
     graph extractor, empty, or missing doc/declaration material before renaming.
   - Rename a symbol when its implementation is cohesive but the name is stale.
   - Rename a file when its declarations are cohesive but the file name is stale.
   - Rename a folder when contained files share a clearer parent concept.
   - Move a file when it fits an existing folder better than its current one.
   - Split a file when candidates show multiple dominant responsibilities.

5. After changes:

   ```bash
   moon info && moon fmt
   moon test
   indexion identity audit .
   ```

The audit is designed to surface review work. Do not maximize the score
mechanically; verify the actual code ownership and references first.
