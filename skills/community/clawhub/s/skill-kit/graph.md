# Skill Graph Extraction

Extract skill dependency edges (frontmatter `depends-on` + topic body `Skill(...)` calls) for a given skill set, then render as Mermaid and optionally dispatch to a force-directed d3 receiver.

## When to Use

- Visualize how skills cross-reference each other before plugin bundling decisions
- Audit cluster boundaries as companion to `cc-plugin/clustering`
- Generate a dependency diagram for documentation deliverables
- Detect outside-set edges (candidate → non-candidate) that signal vendor/pin candidates

## Inputs

| Input | Form | Example |
|-------|------|---------|
| Skill set | list of slugs or `~/.claude/skills/<slug>` paths | `code-workflow github-flow consolidate` |
| `--render=<skill>:<topic>` (optional) | abstract dispatch contract for d3 receiver | `--render=es6kr:force-graph` |
| `--scope=topic\|skill\|both` (optional) | edge granularity (default: `both`) | `--scope=skill` |

## Procedure

### Step 1: Run extract-deps script

```bash
bash ~/.claude/skills/skill-kit/scripts/extract-deps.sh <slug...> > /tmp/edges.json
```

The script:

1. Resolves each slug to `~/.claude/skills/<slug>/` (falls back to `~/.agents/skills/<slug>/`).
2. Parses **frontmatter `depends-on`** (both inline `[a, b]` and YAML block `- name` forms — both must be supported).
3. Greps every `.md` body (SKILL.md included, frontmatter stripped) for two reference forms:
   - `Skill("<name>", ...)` calls
   - `/<name>` slash invocations (word-boundary anchored to avoid matching path segments like `org/repo` or `repos/{owner}/issues`)
4. Filters common false positives (GitHub API URL words like `issues`/`orgs`/`pulls`, generic frontmatter keys, shell paths).
5. Dedups (`source > target`) across frontmatter + body so a target referenced both ways emits once.
6. Emits `{nodes, edges}` JSON to stdout. Each edge carries `{source, target, kind, source_file}` where `kind ∈ {"depends-on", "solid", "outside"}`.

**Why both Skill() AND slash?** Frontmatter `depends-on` is the declared contract but body coupling often outweighs it. Real-world example: `consolidate` declares `depends-on: [superpowers, git-repo]` yet has very-strong body coupling with `github-flow` (`github-flow/merge.md` invokes `Skill("consolidate", "pr-review")` as MANDATORY; `consolidate/next.md` routes to `/github-flow epic-bundle`). Without body-ref extraction, the resulting graph silently misses the strongest edge.

### Step 2: Build Edge Table

Render the JSON as a Markdown table for the documentation deliverable:

```markdown
| From | To | Trigger | Source |
|------|-----|---------|--------|
| skill-a | skill-b | frontmatter depends-on | SKILL.md L6 |
| skill-a/topicX | skill-b/topicY | Skill() call | topicX.md L42 |
| skill-a (in-set) → | external-skill (outside) | outside-set bundle signal | SKILL.md L7 |
```

### Step 3: Mermaid render (always)

Emit a `flowchart TD` block. Group nodes by skill via Mermaid `subgraph`:

```markdown
\`\`\`mermaid
flowchart TD
    subgraph A[skill-a]
        a_topic1[topic1]
        a_topic2[topic2]
    end
    subgraph B[skill-b]
        b_topic1[topic1]
    end
    a_topic1 --> b_topic1
\`\`\`
```

### Step 4: Optional d3 force-directed render (dispatch)

**Caller-supplied dispatch flag** — `--render=<skill>:<topic>` lets the caller decide which receiver owns the d3 template.

```bash
/skill-kit graph <slugs> --render=<receiver-skill>:<receiver-topic>
```

When the flag is supplied, the graph topic invokes the receiver with the edges JSON. The receiver owns the HTML template, force-tuning controls, and convex-hull rendering. **Do NOT hardcode a specific receiver name** — see `portability` Rule B (Generic skills must expose abstract dispatch, not vendor-specific calls).

When the flag is omitted, the procedure stops at the Mermaid + Edge Table deliverable.

### Step 5: Outside-set surfacing (HARD STOP)

Edges where `source ∈ input set` and `target ∉ input set` are **outside-set bundle signals** — not cluster expansion. Emit them in a separate table so the caller can decide vendor vs. cross-plugin pin per `cc-plugin/clustering` outside-set rule:

```markdown
| Outside edge | Source skill | Decision |
|--------------|--------------|----------|
| git-repo → commit-tidy | git-repo (frontmatter depends-on) | vendor / pin / drop |
```

Suppressing outside-set edges silently misses bundle decisions — always surface, never drop.

## Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Hardcode a specific render receiver (e.g., `es6kr:force-graph`) in graph topic body | Use abstract `--render=<skill>:<topic>` dispatch — caller chooses the receiver (Rule B of `portability`) |
| 2 | Limit `depends-on` parser to inline `[a, b]` form only | Support both inline AND YAML block (`- name`) forms — both occur in published skills |
| 3 | Stop at depends-on; ignore topic body `Skill(...)` calls | Both depends-on (skill-level) and `Skill(...)` (topic-level) are edges; topic-granularity reveals hub-and-spoke patterns invisible at skill-level |
| 4 | Render Mermaid with topic-granularity nodes for skills not in the input set | Outside-set edges = bundle signal — emit separately in their own table for vendor/pin decision |
| 5 | Add the graph topic without running `route.md` Step 2b remote-search first | New topic additions must clear the remote-search gate to detect existing published skills with the same capability |
| 6 | Treat `Skill("<slug>", ...)` and `Skill("<slug>:<topic>", ...)` calls as different edge kinds | Both forms target the same skill; topic specifier is metadata, not a separate edge |

## Self-check (HARD STOP — before invoking)

1. Did you run `/skill-kit find <keyword>` and confirm no published skill already covers this capability? (per `route.md` Step 2b)
2. Are edges enumerated from BOTH frontmatter `depends-on` AND topic body `Skill(...)` calls?
3. If d3 render is requested, is it dispatched via the abstract `--render=<skill>:<topic>` flag (not a hardcoded receiver call)?
4. Are outside-set edges surfaced in a separate table rather than silently dropped?
5. Are both inline AND YAML block `depends-on` forms covered by your test inputs?

## Outputs

| Output | Always | When `--render` |
|--------|--------|------------------|
| Edge Table (Markdown) | ✅ | ✅ |
| Mermaid `flowchart TD` block | ✅ | ✅ |
| Outside-set table | ✅ | ✅ |
| d3 force-directed graph (via receiver) | — | ✅ |

## Related

- `route.md` — Step 2b remote-search procedure (HARD STOP gate before adding new topics)
- `portability.md` — Rule B abstract dispatch contract for generic skills
- `cc-plugin/clustering` — plugin-level membership clustering reuses the same edge extraction
- `find.md` — npx skills CLI discovery (primary remote-search receiver)

## Example invocation

```bash
# Mermaid + Edge Table only
/skill-kit graph code-workflow github-flow tdd

# With d3 force-directed render dispatched to a force-graph receiver
/skill-kit graph code-workflow github-flow tdd consolidate --render=es6kr:force-graph

# Skill-level scope only (skip topic body grep)
/skill-kit graph code-workflow github-flow --scope=skill
```
