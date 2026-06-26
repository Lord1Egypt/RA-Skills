---
name: create-skill-from-repo
description: Bootstraps modular Agent Skills from any repository. Clones the source to `sources/`, extracts core documentation into categorized references under `skills/`, and registers the output in the workspace `AGENTS.md`.
metadata:
author: hairy
version: "2026.2.3"
category: "Automation / Knowledge Engineering"
---

# Create Skills from Repo

Use this workflow to quickly ingest a framework or project's logic and documentation into the local environment. This is triggered when a user provides a `<repo-url>` and a `<skills-name>` for which no local skill yet exists.

## 🎯 Objectives

1. **Source Persistence**: Keep the original repo in `sources/` for traceability and future updates.
2. **Knowledge Distillation**: Convert dense documentation into agent-optimized `references/*.md` (focusing on *Usage* and *Why* over *Installation*).
3. **Automatic Registration**: Ensure the new skill is immediately discoverable via `AGENTS.md`.

---

## 🛠 Prerequisites

* **Validation**: Ensure `<repo-url>` is valid and `<skills-name>` uses kebab-case.
* **Environment**: Verify `git` access and identify the project root.

---

## 🔄 Workflow

### Step 1: Source Synchronization

1. Define the destination: `sources/<submodule>`.
2. **Sync Logic**:
* **Primary**: `git submodule add <repo-url> sources/<submodule>`
* **Fallback**: If the workspace is not a git repo, use `git clone --depth 1 <repo-url> sources/<submodule>`
* **Maintenance**: If the directory exists but is empty, run `git submodule update --init`.



### Step 2: Identify Knowledge Base

1. **Locate Source Root**: Scan `sources/<submodule>/` for `docs/`, `wiki/`, `README.md`, or `packages/*/docs/`.
2. **Filtering Strategy**:
* ✅ **Include**: API references, core concepts, design patterns, best practices.
* ❌ **Exclude**: Installation guides (irrelevant to the Agent), contributing logs, sponsorship info, or marketing fluff.



### Step 3: Modular Skill Generation

> **Target Structure**: `skills/<skills-name>/[SKILL.md, GENERATION.md, references/]`

1. **`references/*.md` Guidelines**:
* **Atomicity**: One concept per file.
* **Naming**: `{category}-{concept}.md` (e.g., `core-reactivity.md`).
* **Content**: Must include a `Frontmatter`, a brief description, high-quality **Code Snippets**, and source URLs.


2. **`SKILL.md` Indexing**:
* Create a central entry point with tables categorizing references into `Core`, `Features`, and `Advanced`.


3. **`GENERATION.md` Metadata**:
* Record the Git SHA, source path, and generation date for future diffing.



### Step 4: The Coverage Loop

1. **Review**: Compare the `Source Root` navigation tree against the generated `references/`.
2. **Supplement**: If major modules (e.g., Middleware, Auth, Error Handling) are missing, repeat Step 3 for those specific modules.
3. **Exit Condition**: Stop once the primary API surface and architectural pillars are covered. Do not get bogged down in edge cases.

### Step 5: Integration & Handover

1. **Update `AGENTS.md**`: Locate `AGENTS.md` in the project root (create it if missing).
2. **Inject Skill Entry**:
```markdown
### <skills-name>
- **Location**: `skills/<skills-name>/`
- **Description**: [Short description from SKILL.md]

```


3. **Completion Report**: Summarize the output for the user (e.g., "Generated 15 reference files covering Core and Advanced modules").

---

## 💡 Key Principles

* **Agent-Centric Writing**: Write for an AI audience. Prioritize technical accuracy and code examples over prose.
* **Kebab-Case**: Strictly use `kebab-case` for all directory and filenames.
* **Path Formatting**: Always use forward slashes (`/`) for cross-platform compatibility.
* **Incremental Readiness**: The `sources/` clone should remain so that `git diff` can be used later to spot documentation changes.

---

## 📚 References

| Topic | Description | Reference |
| --- | --- | --- |
| **Coverage Criteria** | Definitions of "major modules" and stop conditions | [coverage-loop](references/coverage-loop.md) |
| **Style Guide** | Detailed writing style for reference files | [style-guide](references/style-guide.md) |

---

**Would you like me to simulate a run of this skill using a specific repository URL to show you the expected output?**