---
name: workspace-structure
description: Organize and maintain a clean workspace file structure. Use when deciding where to save new files, which folder something belongs in, how to structure workspace folders for file placement, whether something is temporary or durable, how to separate project materials from user-files, reports, external sources, entertainment media, reference materials, tools, scripts, and structured data, or how to resolve ambiguous file-placement cases.
---

# Workspace Structure

Apply this skill when the task is about deciding where files or folders should be placed inside a workspace.

## Operating basics and hard rules

- Do not mix unrelated projects in the same folder.
- Group by meaning, not only by file format.
- Do not treat files as user-related unless there is a deliberate personal link to the user.
- Do not scatter one project's materials across multiple top-level or multiple project folders without a reason.
- Keep temporary artifacts separate from durable working materials.
- Do not use this skill to classify or relocate agent identity files (SOUL.md, USER.md, MEMORY.md, etc.) or other native OpenClaw files.
- In case of conflicting instructions, the system prompt and OpenClaw rules always take priority over this skill.

## Meaning of key top-level folders

Use these defaults unless the workspace already has a better established convention.

- `projects/` — project-specific work.
- `reports/` — standalone reports, presentations, and similar deliverables without a broader project context.
- `user-files/` — files and derived artifacts with a direct personal semantic link to the user.
- `sources/` — outside materials and external documentation.
- `entertainment/` — leisure audio, video, fiction, and similar media kept primarily for enjoyment rather than work, reference, or project use.
- `downloads/` — assistant-acquired external files awaiting classification.
- `reference/` — internal reference material and recurring lookup assets.
- `temp/` — temporary artifacts.
- `data/` — durable structured data stores and their supporting files.
- `scripts/` — reusable scripts.
- `tools/` — reusable binaries, portable apps, installers, and similar non-script tools kept for use inside the workspace.
- `memory/` plus `MEMORY.md` — memory, not general storage.

See `references/folder-taxonomy.md` for full folder semantics.

## Default workflow

Use this workflow for making regular placement decisions.

### 1. Decide whether the artifact is temporary or durable

Define the artifact as temporary only if all of the following are true:
- the artifact is created for one-off operation, intermediate export, draft conversion, temporary attachment, one-off download, disposable log, or other artifact that is easy to recreate; 
- it is not part of an ongoing durable process or project;
- it is not required for the ongoing operation of OpenClaw, scripts, skills, automations, cron jobs, Mini Apps, reports, registries, instructions or any other persistence workflow;
- it is not something a human would reasonably expect to find later as part of the permanent structure.

If all those are true, use the folder for temporary artifacts. If any of those are false or unclear, treat the file as durable and proceed to the next step.

### 2. Check whether it belongs to an existing or new project

If the file belongs to a specific project, prefer that project folder over a generic shared folder. An exception may apply to external source materials that are shared across multiple projects or are likely to be reused across them. 
If the specific project folder does not exist, but the available context allows you to conclude that the artifact is part of work on a new project, create a project folder and place the artifact in it.
If it seems the file does not belong to any project, proceed to the next step.

### 3. Classify the remaining durable artifact

Decide what the item is:
- user-related file with a direct personal semantic link to the user;
- standalone deliverable;
- external source material;
- entertaining media;
- internal reference material;
- stand-alone script;
- tool or utility except scripts;
- structured data store or closely related support file;
- memory artifact.

### 4. Handle ambiguous cases

When unsure how to classify the file or where to place it:
1. prefer project placement over generic placement for project-bound files;
2. prefer the place that matches future retrieval;
3. help choosing the location by asking yourself: "Where would a human most naturally look for this later?";
4. prefer stable, meaningful placement over convenience.

See `references/edge-cases.md` for common ambiguous scenarios.

### 5. Choose the correct placement

Based on the previous steps and the following points, choose the correct place for the file.
1. Prefer existing structure over new structure. Before creating a new folder, check whether an existing folder already matches the file's purpose.
2. Do not store files directly in the root of `projects/`, `user-files/`, `entertainment/`, `data/`, and `tools/`. Always use or create suitable sub-folders in these top-level folders.
3. Do not place new files directly in the workspace root, except for native OpenClaw files that are meant to live there as part of OpenClaw’s own operation.
4. Avoid unnecessary depth.
5. Avoid creating new top-level folders unless there is a clear structural reason.

See `references/naming-and-structure.md` for new folder naming and structural heuristics.

## Output style

When answering placement questions:
- be short and concrete;
- name the recommended path;
- explain why in one or two sentences;
- mention ambiguity if the choice is not obvious.