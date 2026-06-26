# Naming and structure

This file defines naming and structural heuristics for a clean workspace.

## Naming principles

- Use names that clearly express purpose.
- Prefer short but specific names.
- Avoid vague names like `misc`, `stuff`, `new`, `other`, `test-final-2`, or `random`.
- Avoid decorative naming that only makes sense to the creator.
- Keep naming patterns consistent inside the same area.

## Folder naming heuristics

Good folder names usually answer one of these questions:
- what this area is for;
- who or what it belongs to;
- what kind of material lives there.

Examples of clearer naming:
- `projects/openclaw-container-migration`
- `reference/workspace-rules`
- `user-files/personal-documents`
- `sources/equipment-manuals`
- `tools/ocr-tool`
- `entertainment/audiobooks`

## Structure principles

- Group by meaning before grouping by file format.
- Keep related materials near each other.
- Do not add depth unless it improves retrieval.
- Do not create a subfolder just because a folder has more than one file.
- Use a subfolder when it creates a stable conceptual grouping.

## Signs of bad structure

- many unrelated materials in one folder;
- top-level clutter;
- duplicate folder meanings;
- forcing extra subfolders where root-level placement is intentionally acceptable;
- creating separate folders for individual files without a clear structural reason;
- project files spread across general-purpose folders for no good reason.

## Signs of good structure

- a human can predict likely file location;
- categories are meaningfully different;
- durable files are not mixed with disposable artifacts;
- project materials live with the project;
- external source material is separated from internal and user-owned material.

## Depth heuristic

Ask whether each additional folder level changes meaning.

If a deeper level only mirrors file format or personal indecision, avoid it.

If it creates a stable category that improves retrieval, it is justified.

## Recommended top-level discipline

Top-level folders should represent durable categories, not momentary convenience.

A top-level folder is justified when:
- it has a clear long-term meaning;
- many future files are likely to belong there;
- it reduces ambiguity;
- it helps humans navigate the workspace.
