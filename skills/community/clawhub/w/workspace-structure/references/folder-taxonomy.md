# Folder taxonomy

This file defines the intended meaning of the main top-level workspace folders.

## projects/

Use `projects/` for work that belongs to a distinct project. A project is an activity that logically has:
- a distinct topic or goal;
- a set of related materials;
- stages of implementation;
- an expected outcome, completion, or major milestones.
Even if a project is long and its endpoint isn't entirely clear, it usually still has identifiable stages: product release, implementation, launch, migration, a series of documents, research, event preparation, etc.

Examples:
- infrastructure migration project notes;
- lecture preparation materials;
- drafts, exports, and helper files for one product launch;
- files for a specific client initiative.

Do not use `projects/` for:
- general user files unrelated to a project;
- reference material used across many contexts;
- temporary artifacts with no project value;
- standalone reports or presentations when there is no broader project context.

## reports/

Use `reports/` for completed or near-complete reports, presentations, analytical deliverables, and research summaries that are not part of an established project.

Examples:
- one-off analytical reports;
- slide decks prepared for delivery;
- research briefs;
- summary documents produced for one task without a broader project folder.

Do not use `reports/` for:
- intermediate artifacts that belong in `temp/`;
- deliverables that are clearly part of an ongoing project;
- files with a direct personal semantic connection to the user that belong in `user-files/`;
- source materials that belong in `sources/`.

The root of `reports/` may be used for one-off standalone deliverables when no further grouping is needed.

## user-files/

Use `user-files/` for durable files and derived artifacts that have a direct personal connection to the user and are not part of one specific project.

This includes more than traditional documents. It can include:
- official documents belonging to the user;
- photos, scans, and saved images with a direct personal connection to the user;
- saved notes created by or for the user;
- files the user explicitly asked to keep as their own materials;
- assistant-produced derivatives of user material, such as retouched photos;
- derived outputs that remain directly about the user, such as a list of the user's favorite songs generated from the user's own activity data.

Do not use `user-files/` for:
- external vendor manuals that belong in `sources/`;
- internal reference material that belongs in `reference/`;
- project-bound artifacts that belong in `projects/`;
- external media copies that belong in `sources/` or `entertainment/`.

Key test: a file belongs in `user-files/` because of its personal semantic connection to the user, not because it is final, useful, or convenient to keep.

## sources/

Use this folder for external materials.

Preferred meaning:
- documentation from vendors or manufacturers;
- equipment manuals;
- datasheets;
- external guides;
- saved articles;
- books, PDFs, and other materials that act as outside sources;
- materials kept for study that are not user-authored working files.

Use `sources/` as the standard top-level folder for broad external material.

The key distinction from `entertainment/` is purpose of use: if the file is kept primarily as a source for work, hobby, reference, or project use, prefer `sources/`.

Do not use this folder for:
- the user's own files;
- internal project artifacts;
- internal reference notes created specifically for this workspace;
- leisure-first media kept primarily for enjoyment.

## reference/

Use `reference/` for internal reference material and recurring lookup assets.

Examples:
- rules and conventions;
- infrastructure notes;
- policies;
- lookup tables;
- durable technical notes used across tasks.

Difference from `sources/`:
- `sources/` contains outside material;
- `reference/` contains internal working reference.

If a file answers the question "Where should I look for a rule, a schema, or precise internal reference information?", it is a candidate for `reference/`.

## temp/

Use `temp/` only for temporary artifacts.

Examples:
- intermediate and one-off exports;
- draft conversions;
- temporary attachments;
- test files;
- disposable logs;
- artifacts that are easy to recreate.

Do not use `temp/` for:
- project documents that matter;
- durable reports;
- rules or instructions;
- files used by scripts or automation on an ongoing basis;
- files that will likely be revisited.

If in doubt, do not use `temp/`.

## data/

Use `data/` for structured data stores and tightly related support files.

Examples:
- sqlite files and other database files;
- registries and operational tracking tables when they function as durable structured storage.

Create a separate subfolder inside `data/` for each distinct database or registry.

The following may be stored along with the database:
- schema;
- auxiliary SQL files;
- documentation on the structure;
- supporting files directly related to that database or registry.

Do not place generic spreadsheets, CSVs, or notes here just because they contain data. However, CSV or spreadsheet files may belong in `data/` when they function as part of a durable structured store, registry, or operational data workflow, rather than as one-off reports or loose working files.

## entertainment/

Use `entertainment/` for leisure audio, video, fiction, and similar media kept primarily for enjoyment.

Examples:
- films and series kept mainly for watching;
- music kept mainly for listening;
- fiction ebooks or audiobooks;
- similar leisure media not primarily kept as sources.

The key distinction from `sources/` is purpose of use: if the file is kept mainly for enjoyment, prefer `entertainment/`. If it is kept mainly as a source for work, hobby, reference, or project use, prefer `sources/`.

## scripts/

Use `scripts/` for reusable scripts and command-line helpers.

Examples:
- shell utilities;
- Python scripts;
- maintenance scripts;
- repeatable helper programs.

If a script belongs only to one project and is easiest to find there, it may live inside that project instead.

## tools/

Use `tools/` for reusable binaries, portable apps, installers, unpacked tool directories, and similar non-script tools kept for ongoing use inside the workspace.

Examples:
- standalone binaries;
- AppImage files;
- unpacked portable utilities;
- reusable installers kept as working tools.

Create a separate subfolder inside `tools/` for each distinct app, tool, or utility. 
Store apps, tools, or utilities together with their related config, examples, license files, and bundled resources.

Do not use `tools/` for:
- ordinary scripts that belong in `scripts/`;
- one-off downloads that still await classification.

## memory/

Use `memory/` and `MEMORY.md` only for memory, not as a general file repository.

## downloads/

Use `downloads/` for externally acquired files saved by the assistant before classification and permanent placement.

Examples:
- files downloaded from the internet before they are clearly classified;
- email attachments fetched by the assistant;
- externally retrieved documents that are not chat attachments staged by OpenClaw in `media/inbound/`;
- other outside files intentionally brought into the workspace for later sorting.

Do not use `downloads/` for:
- chat attachments already staged in `media/inbound/`;
- disposable temporary artifacts that belong in `temp/`.

This folder is a human-facing intake layer for assistant-acquired external files, not a permanent catch-all.
The root of `downloads/` may be used as an intake layer when no further grouping is yet needed. If the final category is immediately obvious, placing the file directly there is also acceptable.

## Additional top-level folders

Use this section to document any additional top-level folders if you decide to introduce them later.
