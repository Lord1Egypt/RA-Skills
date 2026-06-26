---
# Metadata for this configuration
agent_types_reference:
  - openclaw
  - workbuddy
  - codex
  - claude
---

# Skill Search Sources & Strategy

This file defines how to discover existing skills during **Phase 1: Design** (search + compare).  
Search queries are derived from the **understanding** step (user intent, domain, use cases).

The search runs through two **parallel** channels — both are always executed:

1. **Local discovery** (Part 1 + Part 2): Scan installed skills for matches.
2. **Web discovery** (Part 3): Search online platforms for matches.

Results from both channels are collected into a `ref-skills/` folder and summarized for comparison.

---

## Part 1: Configuration Scan

Examine the agent's configuration to identify which skills are enabled.

### OpenClaw & QClaw

- **Configuration**: `~/.openclaw/openclaw.json` (JSON5 format)
- **Skill enablement field**: `skills.entries.<skillKey>.enabled: true/false`
- The `entries` object maps skill names to their configuration. A skill is enabled if this field is present and set to `true`.

### Codex

- **Configuration**: `~/.codex/config.toml` (TOML format)
- **Skill enablement field**: `skills.enabled: true/false`
- Codex can also have per-skill toggles under `[[skills.config]]`, where a specific skill can be disabled without removing its directory.

### WorkBuddy

- **Configuration**: **No standalone config file** — WorkBuddy uses a **directory-as-enablement** model.
- **Skill enablement**: A skill is considered enabled if its `SKILL.md` file exists in either the project-level or user-level skill directory.
- **Structure**: `[workspace]/.workbuddy/skills/` (project-level) and `~/.workbuddy/skills/` (user-level) — each subdirectory must contain a valid `SKILL.md`.

### Action for Part 1

- **If** the configuration file exists **and** contains an explicit list of enabled skills:
  - Extract skill names and their descriptions.
  - Attempt to locate the corresponding skill folder (see Part 2).
- **If** the configuration file **does not exist or contains no enabled skills**:
  - Proceed directly to the **Directory Fallback** process (Part 2).

---

## Part 2: Local Discovery & Collection

Once we have the **name** of an enabled skill (or when no configuration exists), locate its installation folder, read the full `SKILL.md`, and **copy it into the `ref-skills/` folder**.

### Priority Hierarchy

The search order is determined by the following priority levels:

| Priority | OpenClaw / QClaw | WorkBuddy | Codex |
| :--- | :--- | :--- | :--- |
| **Highest** | `<workspace>/skills` (workspace-specific) | `[workspace]/.workbuddy/skills/` (project-level) | `./.codex/skills/` (project-level) |
| **High** | `<workspace>/.agents/skills` (project-level agents) | `~/.workbuddy/skills/` (user-level) | `~/.codex/skills/` (user-level) |
| **Medium** | `~/.agents/skills` (global personal agents) | — | Extra directories via `skills.directory` |
| **Low** | `~/.openclaw/skills` (global managed / shared) | — | — |
| **Lower** | Bundled skills (built-in) | Bundled skills | Bundled skills |
| **Lowest** | `skills.load.extraDirs` (additional directories) | — | — |

- **If a skill is found in a higher-priority directory, lower-priority directories are not checked for that skill name.** This is the "first match wins" algorithm.
- **If multiple configuration-enabled skills exist across different directories**, the one in the highest-priority directory is selected (workspace > user > bundled > extraDirs).

### Action for Part 2

For **each skill** whose name or description suggests relevance to the user's intent:

1. Locate its folder following the priority hierarchy above.
2. Read the `SKILL.md` to confirm relevance.
3. **Copy the `SKILL.md` into `ref-skills/`**, renamed as:

   ```
   local.<skill-name>.SKILL.md
   ```

   Example: `local.wechat.SKILL.md`, `local.obsidian.SKILL.md`

4. Do NOT copy non-matching skills — only those that appear relevant to the user's stated domain or use case.

### Presenting Local Results

For each copied skill, record:
- **Name** and **source path**
- **Enablement status**: Explicit (from config) or implicit (from directory)
- **Output file**: Path within `ref-skills/`

---

## Part 3: Web Discovery & Collection

Run in **parallel** with Part 2. Search online skill platforms for skills matching the user's intent, domain, and use cases.

### Query Derivation

Use the **understanding** from the previous phase (the user's intent, domain, and use cases) to formulate search keywords for each platform.

### Platforms to Search

**CRITICAL**: Each platform requires a SEPARATE WebSearch call.
Do NOT combine multiple `site:` operators in one query — most search engines
(including Brave Search) do not support `site:A OR site:B` syntax.

**Preferred**: Spawn subagents to run all platform searches in parallel.
**Fallback (no subagent)**: Run one WebSearch per platform, sequentially.

Search **each** of the following platforms with a separate query:

1. `clawhub.ai`
2. `skills.sh`
3. `officialskills.sh` (low trust score — verify results before relying on them)
4. `GitHub` (search for repositories relevant to the keywords — not raw `*.md` files)
5. `skillhub.cloud.tencent.com`
6. `https://skillsmp.com`

### Filtering

- Only consider skills with **>500 downloads/installs** (or equivalent popularity metric: stars, forks, "used by" count).
- If a platform does not expose such numbers, use relative comparison (e.g., "significantly more popular than others in the same result set").

### Result Handling

#### Case A: Multiple highly similar skills (overlapping functionality, triggers, I/O)
- Keep only the one with the **highest download count**. Discard the rest.

#### Case B: Partially relevant skills with lower similarity
- **Present a clear, structured list** to the user. Each entry must include:
  - Skill name
  - Source platform (exact URL or platform name)
  - Short description
  - Download count / popularity indicator
  - Key differences compared to the user's stated need
- **Discuss with the user**: ask for their feedback, allow them to select candidates for deeper inspection, or refine the search.

#### Case C: No results or very few low-quality results
- Inform the user that no suitable existing skills were found.
- Suggest moving to **Phase 2: Drafting** (or allow the user to provide custom search parameters/URLs for vertical domains).

### Extended / Vertical Search

- If the user asks for a **domain-specific skill** (e.g., medical imaging, industrial protocols) and the above general search is insufficient:
  - Allow the user to provide **custom URLs** (e.g., academic skill hubs, internal company registries).
  - Perform a search on those URLs.

### Action for Part 3

For each skill identified as relevant from the web search:

1. Fetch its full `SKILL.md` content.
2. **Copy the `SKILL.md` into `ref-skills/`**, renamed as:

   ```
   <platform>.<skill-name>.SKILL.md
   ```

   Examples:
   - `clawhub.awesome-design-md.SKILL.md`
   - `skillsmp.browser-automation.SKILL.md`
   - `github.starlette-admin.SKILL.md`

3. Include only skills confirmed as relevant. Do not copy every search result.

---

## Part 4: Assemble and Summarize

After both Part 2 and Part 3 complete, assemble all results in `ref-skills/` and produce a comparison summary.

### `ref-skills/` Folder Structure Example

```
<skill-name>/.wip/ref-skills/
├── local.wechat.SKILL.md
├── local.obsidian.SKILL.md
├── clawhub.wechat-publisher.SKILL.md
├── skillsmp.article-formatter.SKILL.md
├── github.markdown-exporter.SKILL.md
└── _summary.md
```

### Naming Convention

| Source | Prefix | Example |
| :--- | :--- | :--- |
| Local (Part 2) | `local` | `local.wechat.SKILL.md` |
| clawhub.ai | `clawhub` | `clawhub.skill-creator.SKILL.md` |
| skills.sh | `skillssh` | `skillssh.pdf-toolkit.SKILL.md` |
| officialskills.sh | `officialskills` | `officialskills.image-gen.SKILL.md` |
| GitHub | `github` | `github.react-boilerplate.SKILL.md` |
| skillhub.cloud.tencent.com | `skillhub` | `skillhub.code-review.SKILL.md` |
| skillsmp.com | `skillsmp` | `skillsmp.doc-generator.SKILL.md` |

### Summary (`_summary.md`)

Write `_summary.md` analyzing all discovered results. Structure:

```markdown
# Skill Search Summary

**Search intent**: [user's stated need]
**Date**: [current date]

## 1. Existing Skills Found

| # | Skill | Source | Relevance | Key Differentiator |
|---|-------|--------|-----------|-------------------|
| 1 | wechat | local | High | Publishes to WeChat draft box |

## 2. Non-Skill Resources (Ideas to Borrow)

| # | Resource | Type | Reusable Idea |
|---|----------|------|---------------|
| 1 | article-url | Blog post / Script / Tool | [e.g., "Uses IP proxy rotation on each request"] |

## 3. Gap Analysis: Why No Existing Skill?

| Hypothesis | Evidence | Conclusion |
|------------|----------|------------|
| Too niche / low demand | [e.g., "Search returned 0 results across all 6 platforms"] | Accept / Adjust scope |
| Too complex / hard to generalize | [e.g., "Voting pages vary too much, generic skill is impractical"] | Accept / Narrow scope |
| Legal/ToS risk | [e.g., "vote bots violate most ToS"] | Document risk / Proceed with caution |
| Search missed it | [e.g., "Maybe exists under different keywords"] | Refine and retry |

## 4. Recommendation

[Which skill(s) to use as a base, or whether to create from scratch]
[Direction based on gap analysis: proceed, narrow scope, or abandon]
[Rationale for the recommendation]
```

### What Happens Next

After producing `_summary.md`, append a "Design Context" section to
`workflow-extraction.md`, covering: any useful summary info such as skills found, reusable ideas, and gap analysis.
(If nothing was found, note that in the Design Context.)

Present the summary to the user and ask "Further refine the design using these results?"
(The calling flow — SKILL.md Step 2.3 — gates the refine / proceed decision.)

If proceeding to Phase 2, the summary and Design Context inform whether to:
- **Base the new skill** on the most relevant existing SKILL.md (copy and modify)
- **Borrow patterns** from multiple reference skills (combine approaches)
- **Create from scratch** if no existing skill is close enough

---

## Rule: Source Attribution

**Every skill shown to the user must clearly state its source.**

- For **local paths**: Show the full file system path where the `SKILL.md` was found.
- For **web results**: Show the platform name and the direct URL (if available).
- For **comparison summaries**: Cite the source of each compared skill.

---

## Appendix: Popularity Heuristics per Platform

| Platform | Popularity Field |
| :--- | :--- |
| `skills.sh` | "Installs" / "Used by" |
| `clawhub.ai` | "Downloads" badge |
| `GitHub` | Stars + Forks (combined) |
| `skillsmp.com` | "Popularity" score |
| `officialskills.sh` | "Downloads" (if available) |
| `skillhub.cloud.tencent.com` | "热度" / "下载量" |

If a number is not available, note the absence and use qualitative description (e.g., "this skill appears actively maintained").
