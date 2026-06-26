# Topic Route

Receives a topic description, scans existing skills (local + remote ecosystem), and recommends **which skill and which topic to place it under**.

For **plugin-level clustering** (which *skills* to bundle into a shared plugin, not which *topic* goes in a skill), see `Skill("cc-plugin", "clustering")` — different scope (skill-level placement vs. plugin-level membership), different inputs, different output.

## When to Use

- When unsure "where should this feature go?"
- When you need to decide whether to add a new topic to an existing skill or create a new skill
- Use for "topic routing", "topic placement", "where to put", "topic route"

## Workflow

### 1. Collect Input

Receive the following from the user:

- **Topic description**: What the feature does (e.g., "Helm chart lint")
- **Trigger keywords** (optional): When it should activate (e.g., "helm lint", "chart validation")

### 2. Scan Existing Skills (local + remote — both MANDATORY)

Scanning the **local** install is not enough. A feature you are about to add may
already be **published** by someone in the open ecosystem — reuse beats rebuild.
Run both 2a (local) and 2b (remote) before forming any verdict.

#### 2a. Local scan

```bash
# Collect SKILL.md descriptions from all skills
for dir in ~/.claude/skills/*/; do
  skill_name=$(basename "$dir")
  head -5 "$dir/SKILL.md" 2>/dev/null
done

# Check project skills as well
for dir in .claude/skills/*/; do
  skill_name=$(basename "$dir")
  head -5 "$dir/SKILL.md" 2>/dev/null
done

# Check plugin skills as well
for dir in ~/.claude/plugins/*/skills/*/; do
  skill_name=$(basename "$dir")
  head -5 "$dir/SKILL.md" 2>/dev/null
done
```

#### 2b. Remote ecosystem search (MANDATORY before recommending "build")

Before recommending that a feature be authored (new skill **or** new topic on an
existing skill), search the open skill ecosystem for an existing implementation.
**This skill's own `find` topic is the primary tool** (npx skills CLI →
skills.sh) — invoke it, do not skip it. ClawHub is an optional secondary registry
(a different source).

```text
/skill-kit find <feature keywords>             # primary: this skill's find topic (npx skills → skills.sh)
Skill("clawhub", "find <feature keywords>")    # optional: ClawHub registry (separate source)
```

- Search by **capability keywords**, not by your intended skill name (e.g., "plugin clustering", "skill affinity score", "bundle skills"), since an existing skill may name the same capability differently.
- If a remote skill already covers the capability → prefer **reuse/install** (Verdict D below) over authoring a duplicate.
- Record what you searched and what you found, so the verdict is auditable.

| # | Don't | Do |
|---|-------|-----|
| 1 | Scan only the local install and conclude "no existing feature" | Run 2a (local) **and** 2b (remote `find`/`clawhub`) before any verdict |
| 2 | Search remote only when creating a brand-new skill | Remote-search also before adding a **topic/feature** to an existing skill — capability duplication is the risk, not just name collision |
| 3 | Search by the skill name you plan to use | Search by capability keywords — the same feature may be published under a different name |

### 3. Matching Criteria

Select candidates based on the following criteria:

| Criteria | Weight | Description |
|----------|--------|-------------|
| Existing implementation (local OR remote-published) | Highest | If a local skill or a remote-published skill (from 2b) already covers the capability, reuse beats authoring a duplicate |
| Domain match | High | Same tool/area (e.g., helm, k3s, git) |
| Relevance to existing topics | High | Whether it forms a logical group with existing topics |
| Description keyword similarity | Medium | Whether trigger keywords overlap |
| Topic count limit | Low | Consider splitting if a skill has 10+ topics |

### 4. Verdict Types

#### A. Add Topic to Existing Skill

The most ideal case. Matches the domain of an existing skill.

```text
Recommendation: Add "lint" topic to helm-makefile-standard skill
Reason: Helm-related features already exist, and lint belongs to the same build tool area as makefile
```

#### B. Merge into Existing Topic (Add Section)

When it's not large enough to warrant a separate topic.

```text
Recommendation: Add "network diagnostics" section to the health topic of k3s skill
Reason: Too small to separate as an independent topic; it's part of health checks
```

#### C. Create New Skill

When it doesn't fit anywhere in existing skills. **Before creating, check slug availability via Skill tool (3rd recurrence — HARD STOP):**

```text
Skill("clawhub", "slug <slug-name>")
```

| # | Don't | Do |
|---|-------|-----|
| 1 | Check slug occupancy via `npx skills search` | Call `Skill("clawhub", "slug <name>")` |
| 2 | Run `curl -sI clawhub.ai/skills/<name>` directly | Call `Skill("clawhub", "slug <name>")` |
| 3 | Read slug.md and run curl commands manually | Call `Skill("clawhub", "slug <name>")` |
| 4 | Assume "no slug-occupancy concept" | clawhub.ai uses slug occupancy (307 = occupied, 200 = available) |

```text
Recommendation: Create new skill "docker-compose"
Reason: no existing docker-related skill; /clawhub slug "docker-compose" = available
```

#### D. Reuse an Existing Remote Skill (do not rebuild)

When the 2b remote search surfaces a published skill that already covers the
capability. Authoring a duplicate is the failure mode this verdict prevents.

```text
Recommendation: Install existing skill "{remote-skill}" instead of authoring
Reason: 2b remote search (find/clawhub) found {remote-skill} covering this capability — reuse over rebuild
```

### 5. Present Results via AskUserQuestion

```text
AskUserQuestion {
  question: "Here's the placement recommendation for topic '{topic_name}'. Where should it go?",
  options: [
    { label: "Reuse remote skill {X}", description: "2b remote search found existing coverage — install over rebuild" },
    { label: "Add topic to {skillA}", description: "Domain match, N existing topics" },
    { label: "Add as section in {topicB} of {skillB}", description: "Similar feature already exists" },
    { label: "Create new skill", description: "No local or remote skill covers it" }
  ]
}
```

Include the "Reuse remote skill" option whenever 2b surfaced a candidate. Omit it only when the remote search returned nothing.

### 6. Follow-up Action Chaining (HARD STOP — Skill tool call required when SKILL.md is touched)

Automatically chain based on selection. **Any flow that modifies `SKILL.md` (frontmatter, Topics table, depends-on, version) MUST be routed through `Skill("skill-kit", "upgrade/writer ...")`** so the upgrade/writer verification procedures (Language Check, depends-on auto-detect, description length budget, version-bump AskUserQuestion, lint) run. Direct `Edit`/`Write` on `SKILL.md` bypasses these gates and is forbidden.

In-topic-only changes (touching one topic `.md` file, no `SKILL.md` change) are exempt: direct `Edit` is allowed because the routed upgrade/writer flow has nothing additional to verify in that case.

| Selection | Chained Action | Touches `SKILL.md`? |
|-----------|----------------|---------------------|
| Add topic to existing skill | `Skill("skill-kit", "upgrade <skill-name> - <topic description>")` | Yes (Topics table + description) |
| Add section inside an existing topic file (no `SKILL.md` change) | Direct `Edit` allowed (in-topic-only exemption) | No |
| Create new skill | `Skill("skill-kit", "writer")` | Yes (new SKILL.md) |

| # | Don't | Do |
|---|-------|-----|
| 1 | Write/Edit SKILL.md + topic files directly after route result | Call `Skill("skill-kit", "upgrade ...")` → upgrade procedure verifies version bump |
| 2 | "I know the upgrade procedure, just do it manually" thinking | Skill tool call enforces procedure compliance. Manual = bypass |

## Example

### Input

> "A topic for automatically handling syncthing conflict files"

### Scan Results

```text
- sync skill: has syncthing topic (chezmoi + syncthing synchronization)
- syncthing-conflict skill: dedicated skill already exists!
- chezmoi skill: dotfile related
```

### Verdict

```text
A syncthing-conflict skill already exists.
→ Add the new feature as a topic to that skill, or enhance the existing SKILL.md.
```

## Notes

- Consider the 1024-character description limit; recommend splitting skills with too many topics
- Also suggest placing in agents (`.claude/agents/`) when more appropriate
  - Complex multi-step tasks → Agent
  - Simple guides/procedures → Skill topic
- If there's overlap with plugin skills, suggest the `dedup` topic
