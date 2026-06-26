---
name: Security Analyst Improvements
overview: Reduce duplication of effort, implement a Level-of-Detail (LOD) report architecture to save context space across agent context windows, extract shared boilerplate, unify terminology, slim entry points, and add missing pieces.
todos:
  - id: phase-1-idor
    content: "Phase 1a: Add boundary directives to IDOR/AuthZ agents (attack-surface-http.md, attack-surface-authz.md, logic-authz-escalation.md)"
    status: pending
  - id: phase-1-rate
    content: "Phase 1b: Add rate-limiting deferral note to attack-surface-http.md"
    status: pending
  - id: phase-1-llm
    content: "Phase 1c: Add conditional LLM deferral to logic-pipeline-exploit.md and git-history-injections.md"
    status: pending
  - id: phase-1-critic
    content: "Phase 1d: Clarify self-check vs critic in exploit-developer.md"
    status: pending
  - id: phase-2-lod-templates
    content: "Phase 2a: Update templates/finding.md with LOD-0, LOD-1, LOD-2 format definitions"
    status: pending
  - id: phase-2-agent-common
    content: "Phase 2b: Create templates/agent-common.md with shared output instructions (LOD writing + incidental findings)"
    status: pending
  - id: phase-2-orchestrator
    content: "Phase 2c: Update orchestrator: add FINDINGS_DIR constant, LOD-aware spawning pattern, index builder, LOD-0 passing between groups"
    status: pending
  - id: phase-2-wave-template
    content: "Phase 2d: Update templates/wave-report.md to use LOD-0 table + atomic file references"
    status: pending
  - id: phase-2-prompts
    content: "Phase 2e: Update all 20 prompt files — replace incidental section with placeholder, replace output instructions with LOD-aware pattern"
    status: pending
  - id: phase-2-terminal
    content: "Phase 2f: Update exploit-developer.md, finding-critic.md, report-writer.md for LOD-aware input (LOD-1 index in prompt, LOD-2 via selective Read)"
    status: pending
  - id: phase-3-mapping
    content: "Phase 3a: Add Phase-to-Group mapping table and rename Wave->Group in security-analyst.md"
    status: pending
  - id: phase-3-skill
    content: "Phase 3b: Update SKILL.md wave references to Group"
    status: pending
  - id: phase-3-full
    content: "Phase 3c: Update full.md wave references to Group"
    status: pending
  - id: phase-4-slim-full
    content: "Phase 4a: Slim full.md to ~20 lines"
    status: pending
  - id: phase-4-slim-recon
    content: "Phase 4b: Slim recon.md to ~20 lines"
    status: pending
  - id: phase-5-threat
    content: "Phase 5a: Create prompts/threat-model-agent.md and update threat-model.md to use it"
    status: pending
  - id: phase-5-dedup
    content: "Phase 5b: Add deduplication guidance with known overlap areas to security-analyst.md"
    status: pending
  - id: phase-5-plugin
    content: "Phase 5c: Add plugin conflict guidance to plugins/README.md"
    status: pending
  - id: phase-6-skill
    content: "Phase 6: Update SKILL.md — directory listing, LOD architecture docs, context budget note"
    status: pending
isProject: false
---

# Security Analyst Suite Improvements

## Scope

All edits within `.claude/skills/security-analyst/`. Two major themes:

1. **Reduce duplication** -- clarify agent boundaries so overlapping agents defer rather than re-analyze
2. **LOD architecture** -- agents write atomic findings to disk and return one-line summaries, saving 80-96% of context space in orchestrator and downstream agent prompts

---

## Phase 1: Clarify Agent Boundaries (eliminate redundant analysis)

Adds 2-5 lines of boundary directives to overlapping agents so they know what to analyze vs. defer. No structural changes.

### 1a. IDOR/AuthZ overlap (3 agents doing the same IDOR check)

**[prompts/attack-surface-http.md](prompts/attack-surface-http.md)** -- Replace the deep IDOR sub-task (lines 44-46) in the "For EACH authenticated endpoint" section with a lightweight flag-and-defer:

```markdown
3. **Authorization / IDOR (flag only)**: Note whether the endpoint verifies caller ownership of the requested resource. Do NOT perform deep IDOR analysis here — the dedicated `logic-authz-escalation` agent (Group 2) will trace every authorization decision in depth. Flag endpoints where ownership checks appear missing as "IDOR-suspect" for Group 2 to investigate.
```

**[prompts/attack-surface-authz.md](prompts/attack-surface-authz.md)** -- Remove Task 6 ("Business Logic Authorization") entirely (lines 53-59). Replace with a deferral note:

```markdown
### Task 6: Server-Side Authorization (deferred)

Server-side function authorization (ownership checks, tier enforcement, cross-endpoint bypass) is analyzed in depth by the `logic-authz-escalation` agent in Group 2. Focus here on database/rules-level authorization only.
```

**[prompts/logic-authz-escalation.md](prompts/logic-authz-escalation.md)** -- Add a note at the top of the Analysis Tasks section:

```markdown
**Note:** Group 1's HTTP and AuthZ agents flag "IDOR-suspect" endpoints and database-level authorization gaps. Read their findings from `{PRIOR_FINDINGS_SUMMARY}` (LOD-0 summaries) and `Read` the relevant LOD-2 finding files to deepen the analysis on flagged endpoints rather than re-scanning from scratch.
```

### 1b. Rate limiting / DoS overlap

**[prompts/attack-surface-http.md](prompts/attack-surface-http.md)** -- In the rate limiting sub-tasks (items 5 and 6), add:

```markdown
Note: Flag rate limiting gaps for the `logic-dos` agent (Group 2) to assess amplification impact. Do not estimate attacker-vs-defender cost here.
```

### 1c. LLM/AI overlap (3 agents covering prompt injection)

**[prompts/logic-pipeline-exploit.md](prompts/logic-pipeline-exploit.md)** -- Rewrite Task 3 (lines 40-48) to defer:

```markdown
### Task 3: AI/ML Manipulation (defer to dedicated agent if present)

If a dedicated `attack-surface-llm` agent ran in Group 1, read its LOD-0 findings from `{PRIOR_FINDINGS_SUMMARY}` and `Read` the relevant LOD-2 finding files. Focus on:
- How AI output flows through the **pipeline** into decisions and actions (downstream impact)
- Whether pipeline validation catches malformed AI output
- Do NOT re-analyze prompt injection or OWASP LLM categories -- those are covered by the LLM agent

If NO LLM agent ran (e.g., focused mode without AI scope), perform the full AI analysis:
1. Read the AI integration code...
(keep existing sub-points as fallback)
```

**[prompts/git-history-injections.md](prompts/git-history-injections.md)** -- Rewrite the "AI/Prompt Injection Variants" sub-section (lines 60-64) to defer:

```markdown
**AI/Prompt Injection Variants (defer if LLM agent active):**
- If the `attack-surface-llm` agent is running in this execution group, defer AI/prompt injection analysis to it — it covers OWASP LLM01 in depth
- Only analyze AI injection here if the LLM agent was skipped (no AI integration detected by recon) but you discover AI-adjacent patterns in git history
```

### 1d. Exploit Developer vs Finding Critic verification overlap

**[prompts/exploit-developer.md](prompts/exploit-developer.md)** -- Rewrite Task 4.5 header (line 79):

```markdown
### Task 4.5: Self-Check (pre-critic sanity pass)

Before writing findings to disk, do a quick self-check on each fix. This is NOT a substitute for the critic agent's thorough review — it catches obvious issues so the critic can focus on deeper validation.

1. Read the surrounding code context (10 lines above and below)
2. Quick check: does the fix obviously break callers or introduce a new vuln?
3. Quick check: does the fix follow the project's existing patterns?
4. If you find an obvious issue, revise the fix. Note "self-revised" in the finding.
```

---

## Phase 2: LOD Architecture + Shared Boilerplate

This is the core architectural change. Agents write atomic finding files to disk and return only LOD-0 summaries. The orchestrator builds an index and passes LOD-0 to downstream agents, who selectively `Read` LOD-2 files from disk when they need full detail.

### Context savings model

Each sub-agent and the orchestrator manage independent context windows. Currently, full findings text (~800 tokens each) gets injected into every downstream agent's prompt AND accumulates in the orchestrator's context. With LOD:


| Context Window                  | Before (25 findings)  | After (LOD)                               | Savings       |
| ------------------------------- | --------------------- | ----------------------------------------- | ------------- |
| Orchestrator (across 23 agents) | ~20K tok accumulated  | ~750 tok (LOD-0 returns)                  | 96%           |
| Each Group 2 agent prompt (x4)  | ~20K tok injected     | ~750 tok (LOD-0) + selective reads        | 81%           |
| Each Group 3 agent prompt (x4)  | ~30K tok injected     | ~1.2K tok + selective reads               | 90%           |
| Exploit dev / critic prompt     | ~30K tok all findings | ~2.5K tok (LOD-1 index) + selective reads | 87% on prompt |


Agents that need full detail (exploit dev, critic, report writer) still consume it via `Read` tool calls. The key difference: prompt injection consumes tokens upfront and limits the agent's working space; tool-based reading is incremental and selective.

### LOD level definitions


| Level | Content                                                                        | ~Tokens/finding | When to use                              |
| ----- | ------------------------------------------------------------------------------ | --------------- | ---------------------------------------- |
| LOD-0 | `ID                                                                            | Severity        | One-sentence summary`                    |
| LOD-1 | ID + title + severity + CVSS + CWE + ATT&CK + file:line + one paragraph        | 100             | Exploit dev/critic triage, finding index |
| LOD-2 | Full finding: attack steps, PoC, exploit scoring, remediation, regression test | 800             | Atomic file on disk, read on demand      |


### 2a. Update finding template with LOD format definitions

**[templates/finding.md](templates/finding.md)** -- Add a new section at the top, before the existing "Individual Finding" section:

```markdown
# Finding Report Format — Level of Detail (LOD)

Findings are written as **atomic files** to `{FINDINGS_DIR}/`. Each file contains the full LOD-2 finding. Agents return LOD-0 summaries to the orchestrator. The orchestrator builds an index with LOD-0 and LOD-1 views.

## LOD-0: One-Line Summary (returned to orchestrator)

Format: `| [FINDING-ID] | [Severity] | [One-sentence description] |`

Example: `| P1-HTTP-001 | High | Unauthenticated webhook endpoint allows attacker to enqueue arbitrary processing tasks |`

## LOD-1: Finding Brief (for index file)

    ### [FINDING-ID]: [Title]
    **Severity:** [S] | **CVSS:** [Score] | **CWE:** [ID] | **ATT&CK:** [TID] | **File:** [path:line]
    [One-paragraph description of the vulnerability and its impact]

## LOD-2: Full Finding (atomic file on disk)
```

Then keep the existing full finding format (everything currently in the file) as the LOD-2 definition. The existing content is unchanged, just reframed as "LOD-2".

### 2b. Create shared agent output template

**Create [templates/agent-common.md](templates/agent-common.md):**

```markdown
# Shared Agent Output Instructions

## Finding Output (LOD Architecture)

For each finding you discover:

1. **Write the atomic finding file** to `{FINDINGS_DIR}/{FINDING-ID}.md` using the LOD-2 format from `{FINDING_TEMPLATE_PATH}`
2. **Build your LOD-0 summary table** — one row per finding: `| [ID] | [Severity] | [One-sentence summary] |`

When you are done with all analysis, return ONLY the following to the orchestrator:

```

## Agent: {AGENT_NAME}

**Endpoints/items analyzed:** [count]
**Findings:** [count] ([severity breakdown])

### LOD-0 Summary


| ID          | Severity | Summary        |
| ----------- | -------- | -------------- |
| P1-HTTP-001 | High     | [one sentence] |
| P1-HTTP-002 | Medium   | [one sentence] |


### IDOR-Suspect Endpoints (if applicable)

[list of endpoints flagged for Group 2 deep dive]

### Incidental Findings

[IX-prefixed findings in abbreviated format]

```

Do NOT send full finding details in your return message. They are on disk.

## Reading Prior Findings

Your `{PRIOR_FINDINGS_SUMMARY}` contains LOD-0 summaries from earlier execution groups. If you need full detail on a specific finding:

1. Note the finding ID from the LOD-0 table
2. `Read` the file at `{FINDINGS_DIR}/{FINDING-ID}.md` for the full LOD-2 content
3. Only read findings relevant to your analysis — do not read all of them

## Incidental Findings

While performing your primary analysis, you may discover security issues OUTSIDE your focus area:

- Use finding ID prefix `IX-{AGENT_PREFIX}-XXX` (IX = incidental)
- Use abbreviated format (severity, file:line, one-paragraph description, ATT&CK technique if obvious)
- Do NOT write atomic files for incidentals — include them in your return message only
- Do NOT let incidental findings distract from your primary analysis
```

### 2c. Update orchestrator for LOD

**[security-analyst.md](security-analyst.md)** -- Multiple edits:

**Constants block (line 38)** -- add:

```markdown
FINDINGS_DIR = {RUN_DIR}/findings
FINDINGS_INDEX = {FINDINGS_DIR}/index.md
```

**Step 1 (line 58)** -- add to mkdir:

```markdown
Bash: mkdir -p {RUN_DIR} {FINDINGS_DIR}
```

**Agent Spawning Pattern (line 293)** -- replace the current pattern with LOD-aware version:

```markdown
## Agent Spawning Pattern

For each agent, the spawning pattern is:

1. Read the prompt template: Read {PROMPTS_DIR}/{prompt-file}.md
2. Read the finding template: Read {TEMPLATES_DIR}/finding.md
3. Read the shared output template: Read {TEMPLATES_DIR}/agent-common.md
   - Replace {AGENT_PREFIX} with the agent's finding ID prefix (e.g., HTTP, AUTHZ, INJ)
   - Replace {AGENT_NAME} with the agent's display name
4. Collect plugin sections (same as before — see Step 3.5)
5. Construct the prompt by replacing ALL placeholders:
   - {RECON_REPORT_PATH}, {FINDING_TEMPLATE_PATH}, {PRIOR_FINDINGS_SUMMARY}, {PLUGIN_CHECKS} (existing)
   - {FINDINGS_DIR} → absolute path to findings directory (NEW)
   - {INCIDENTAL_FINDINGS_SECTION} → content from agent-common.md (NEW)
   - Append the agent-common.md output instructions to the end of the prompt
6. Spawn: Task tool (same as before)
7. Receive the agent's LOD-0 summary return message (small — no full findings)
```

**Consolidation Between Waves (line 283)** -- rewrite for LOD:

```markdown
## Consolidation Between Execution Groups

After each execution group:
1. Collect LOD-0 summary tables from all agents in the group
2. Read `{FINDINGS_DIR}/` to verify atomic finding files were written
3. Deduplicate: if two agents wrote findings for the same vulnerability, keep the more detailed LOD-2 file and delete the other. Update LOD-0 tables accordingly
4. Build/update `{FINDINGS_INDEX}`:
   - **LOD-0 section**: Concatenated LOD-0 tables from all groups so far
   - **LOD-1 section**: For each finding, read its LOD-2 file and extract the LOD-1 brief (first 5 lines: ID, title, severity, CVSS, CWE, ATT&CK, file:line, one-paragraph)
5. Enrich: add cross-references between related findings in the index
6. Prepare `{PRIOR_FINDINGS_SUMMARY}` for next group: the LOD-0 table only, plus `{FINDINGS_DIR}` path for selective reading
7. Collect incidental findings (IX-prefixed) from agent return messages
8. Write the execution group report using `{WAVE_REPORT_TEMPLATE}`
```

**Known Overlap Areas** -- add after Consolidation (new section from Phase 5b, placed here since it's part of consolidation):

```markdown
### Known Overlap Areas

When deduplicating between execution groups, pay special attention to:

- **IDOR/AuthZ**: Group 1's HTTP and AuthZ agents flag suspect endpoints (shallow). Group 2's authz-escalation agent deepens the analysis (LOD-2). Merge by keeping the deeper Group 2 findings and removing Group 1 flags that were fully investigated.
- **Rate limiting/DoS**: Group 1's HTTP agent flags missing rate limits. Group 2's DoS agent assesses amplification and cost. Merge by promoting the DoS agent's finding and removing the HTTP agent's bare flag.
- **AI/LLM**: Group 1's LLM agent covers OWASP categories. Group 2's pipeline agent covers downstream pipeline impact. These are complementary — keep both, cross-reference in the index.
```

### 2d. Update wave report template

**[templates/wave-report.md](templates/wave-report.md)** -- Replace `{WAVE_FINDINGS}` inline block with LOD-0 table + references:

```markdown
## Findings

### Summary (LOD-0)

| ID | Severity | Summary |
|----|----------|---------|
{LOD0_TABLE}

### Finding Details

Full LOD-2 findings are in `{FINDINGS_DIR}/`. To read any finding: `Read {FINDINGS_DIR}/{FINDING-ID}.md`

{IX_FINDINGS}
```

### 2e. Update all 20 prompt files

In each prompt file under `prompts/`, make two changes:

1. **Replace the "Incidental Findings" section** (last ~6 lines of every file) with:

```markdown
{INCIDENTAL_FINDINGS_SECTION}
```

1. **Replace the "Output Format" / "Send your findings" section** with a reference to the shared output template:

```markdown
## Output

Follow the LOD output instructions appended to this prompt. Write each finding as an atomic LOD-2 file to `{FINDINGS_DIR}/{FINDING-ID}.md`. Return only your LOD-0 summary table to the orchestrator.

Finding IDs: Use prefix `{PHASE_PREFIX}` (e.g., P1-HTTP-XXX, P2-INJ-XXX, etc.)
```

The `{PHASE_PREFIX}` values remain the same as currently defined in each prompt. Only the output mechanics change.

### 2f. Update terminal agents for LOD-aware input

These agents consume ALL findings rather than a subset, so they need LOD-1 in their prompt and selective LOD-2 reads.

**[prompts/exploit-developer.md](prompts/exploit-developer.md)** -- Update "Your Inputs" section:

```markdown
## Your Inputs

1. **Recon Report**: Read `{RECON_REPORT_PATH}` for project context
2. **Finding Index**: `{ALL_FINDINGS}` contains the LOD-1 briefs for every Medium+ finding from Groups 1-3
3. **Atomic Finding Files**: Full LOD-2 details are in `{FINDINGS_DIR}/`. For each finding you develop an exploit for, `Read {FINDINGS_DIR}/{FINDING-ID}.md` to get attack steps, affected code, and context
4. **Finding Template**: Follow the format in `{FINDING_TEMPLATE_PATH}`
```

And update Task 1 (Triage) to work from LOD-1:

```markdown
### Task 1: Triage Findings

Review the LOD-1 index from `{ALL_FINDINGS}`:
1. Sort by severity (Critical > High > Medium)
2. Group related findings (same component, same attack surface, same root cause)
3. Identify findings that might chain together
4. For each finding you will develop: `Read {FINDINGS_DIR}/{FINDING-ID}.md` for full LOD-2 context
```

**[prompts/finding-critic.md](prompts/finding-critic.md)** -- Same pattern. Update inputs:

```markdown
2. **Exploit Catalog**: `{ALL_FINDINGS}` contains LOD-1 briefs for all findings from Groups 1-4 with PoCs
3. **Atomic Finding Files**: Full LOD-2 details in `{FINDINGS_DIR}/`. `Read` each finding file to verify exploitability against source code
```

**[prompts/report-writer.md](prompts/report-writer.md)** -- Same pattern. Update inputs:

```markdown
2. **Validated Findings**: `{ALL_FINDINGS}` contains LOD-1 briefs for all critic-validated findings
3. **Atomic Finding Files**: Full LOD-2 details in `{FINDINGS_DIR}/`. `Read` each finding for the final report
```

---

## Phase 3: Unify Phase/Wave Terminology

Phase numbers are embedded in finding IDs (`P1-HTTP`, `P2-INJ`, `P5-DEP`, `P6-CFG`) across all prompts and cannot change. Waves are only referenced in the orchestrator and entry points. Strategy: keep Phase numbers; rename "Wave" to "Execution Group" in the orchestrator and add a mapping table.

### 3a. Add mapping table to orchestrator

**[security-analyst.md](security-analyst.md)** -- Add after the "Constants" block:

```markdown
### Phase-to-Execution-Group Mapping

Phases are the logical analysis categories (and determine finding ID prefixes). Execution Groups are how phases are scheduled (dependency-ordered).

| Execution Group | Phases Included | Why Grouped |
|----------------|----------------|-------------|
| Group 0 | Phase 0 (Recon) | Must complete before all others |
| Group 1 | Phases 1, 2, 5, 6 | Independent; no cross-dependencies |
| Group 2 | Phase 3 (Business Logic) | Needs Group 1 findings |
| Group 3 | Phase 4 (Data Flow) | Needs Groups 1+2 findings |
| Group 4 | Phase 7 (Exploits) | Needs all prior findings |
| Group 4.5 | Phase 7.5 (Critic) | Needs exploit catalog |
| Group 5 | Phase 8 (Report) | Needs validated findings |
| Post | Phase 9 (Fix Plan) | Needs final report |
```

Then rename all "WAVE N" headers in Steps 2-8.5 to "EXECUTION GROUP N". Find-and-replace "WAVE" -> "EXECUTION GROUP" in 8 section headers.

### 3b. Update SKILL.md wave references

**[SKILL.md](SKILL.md)** -- In the "Wave-Based Pipeline" diagram (lines 36-67), rename "Wave" to "Group" and add: "Groups are execution-order groupings of phases. Finding IDs use Phase numbers (P1-P9)."

### 3c. Update full.md wave references

**[full.md](full.md)** -- Rename "Wave" to "Group" in the step list (lines 26-33).

---

## Phase 4: Slim Redundant Entry Points

### 4a. Slim full.md

**[full.md](full.md)** -- Replace the current 52-line file with a ~20-line version:

```markdown
---
description: "Complete 9-phase offensive security analysis. No prompts — runs everything."
model: opus
---

# Security Analyst — Full Analysis

Run the complete analysis with no interactive prompts.

**Settings:**
- Scope: Full — all phases, all attack surfaces
- Output: Files to `docs/security/runs/{YYYY-MM-DD-HHMMSS}/`
- Agent skipping: Only if recon determines irrelevance (e.g., no frontend)

**Execution:** Follow the orchestration flow in `security-analyst.md` with these settings.

**Output files:** See `security-analyst.md` Step 9 for the full file list.

**Expected duration:** 23+ agents across 6 execution groups. Significant processing time.
```

### 4b. Slim recon.md

**[recon.md](recon.md)** -- Replace with ~20-line version:

```markdown
---
description: "Quick security reconnaissance — maps attack surface without vulnerability analysis."
model: opus
---

# Security Analyst — Reconnaissance Only

Run Phase 0 only. Produces a structured security map without vulnerability analysis.

**Execution:** Follow `security-analyst.md` Steps 1-2 (create run dir, spawn recon agent). Stop after recon completes.

**Output:** `docs/security/runs/{YYYY-MM-DD-HHMMSS}/recon-report.md`

**Next steps:** `/security-analyst:full` for complete analysis, `/security-analyst:focused [component]` to target a specific area.
```

---

## Phase 5: Add Missing Pieces

### 5a. Create threat-model agent prompt

**Create [prompts/threat-model-agent.md**](prompts/threat-model-agent.md) (~80-100 lines):

- Accept `{RECON_REPORT_PATH}` and `{OUTPUT_PATH}` as inputs
- Task 1: STRIDE analysis for each trust boundary from the recon report
- Task 2: Attack trees for each crown jewel (root = "Compromise X", branches = attack paths)
- Task 3: Risk matrix (likelihood x impact for each threat)
- Output: Write `{OUTPUT_PATH}` (threat-model.md)
- Use the same offensive framing as other agents
- Follows LOD output conventions for any findings discovered during threat modeling

Update **[threat-model.md](threat-model.md)** execution step 3 to spawn this agent via Task tool.

### 5b. Add plugin conflict guidance

**[plugins/README.md](plugins/README.md)** -- Add a new section after "Creating a New Plugin":

```markdown
## Plugin Overlap and Conflicts

When multiple plugins inject sections for the same agent (e.g., both Next.js and React inject `## attack-surface-frontend`), the orchestrator concatenates all matching sections. Agents should:

- Treat multiple plugin sections as **complementary** checks — run all of them
- If checks conflict, prefer the **more specific** plugin (e.g., Next.js over React for Next.js projects)
- Report the plugin source in findings so the orchestrator can trace which plugin triggered the check
```

---

## Phase 6: Update SKILL.md

**[SKILL.md](SKILL.md)** -- Three additions:

### 6a. Update directory listing (lines 149-195) to include:

- `templates/agent-common.md` (shared LOD output + incidental findings instructions)
- `prompts/threat-model-agent.md`

### 6b. Add LOD architecture documentation after "Key Principles":

```markdown
### Level of Detail (LOD) Architecture

Agent reports use a three-tier Level of Detail system to minimize context consumption across independent agent context windows:

| Level | Content | ~Tokens | Where it lives |
|---|---|---|---|
| LOD-0 | `ID \| Severity \| One sentence` | 30/finding | Agent return message, orchestrator context, `{PRIOR_FINDINGS_SUMMARY}` |
| LOD-1 | ID + title + severity + CVSS + CWE + file:line + paragraph | 100/finding | `{FINDINGS_DIR}/index.md`, terminal agent prompts |
| LOD-2 | Full finding with PoC, remediation, regression test | 800/finding | `{FINDINGS_DIR}/{FINDING-ID}.md`, read on demand |

**How it flows:**
1. Analysis agents write atomic LOD-2 files to `{FINDINGS_DIR}/` and return LOD-0 summaries
2. The orchestrator builds `{FINDINGS_DIR}/index.md` with LOD-0 + LOD-1 views
3. Next-group agents receive LOD-0 in their prompt; selectively `Read` LOD-2 files for relevant findings
4. Terminal agents (exploit dev, critic, report writer) receive LOD-1 index; `Read` all LOD-2 files

This saves 80-96% of prompt tokens for downstream agents while preserving full detail on disk.
```

### 6c. Add context budget note (replaces the simpler version from old Phase 5d):

```markdown
### Context Budget Considerations

The LOD architecture mitigates most context pressure, but be aware:
- The LLM agent prompt (`attack-surface-llm.md`) is ~340 lines before plugin injection — the largest single prompt
- Terminal agents (exploit dev, critic, report writer) still read all LOD-2 files via tool calls; for runs with 40+ findings, consider batching reads
- Plugin sections add to every injected agent's context — keep plugins concise
```

---

## Disk Structure After Changes

```
{RUN_DIR}/
├── findings/                         # NEW: atomic LOD-2 finding files
│   ├── index.md                      # NEW: LOD-0 table + LOD-1 briefs (built by orchestrator)
│   ├── P1-HTTP-001.md               # Written by surface-http agent
│   ├── P1-HTTP-002.md
│   ├── P2-INJ-001.md               # Written by history-injections agent
│   └── ...
├── recon-report.md                   # Unchanged
├── group-1-attack-surface.md        # RENAMED from wave-1, now contains LOD-0 table + refs
├── group-2-business-logic.md        # RENAMED from wave-2
├── group-3-data-flow.md             # RENAMED from wave-3
├── group-4-exploits.md              # RENAMED from wave-4
├── group-4.5-critic-review.md       # RENAMED from wave-4.5
├── security-analyst-final-report.md          # RENAMED from wave-5
├── fix-plan.md                       # Unchanged
└── threat-model.md                   # If threat-model mode used
```

---

## Files Changed Summary


| File                                | Change Type                                                                  | Phase      |
| ----------------------------------- | ---------------------------------------------------------------------------- | ---------- |
| `prompts/attack-surface-http.md`    | Edit (boundary directives + LOD output)                                      | 1a, 1b, 2e |
| `prompts/attack-surface-authz.md`   | Edit (remove Task 6 + LOD output)                                            | 1a, 2e     |
| `prompts/logic-authz-escalation.md` | Edit (prior-findings note + LOD output)                                      | 1a, 2e     |
| `prompts/logic-pipeline-exploit.md` | Edit (conditional defer + LOD output)                                        | 1c, 2e     |
| `prompts/git-history-injections.md` | Edit (defer AI injection + LOD output)                                       | 1c, 2e     |
| `prompts/exploit-developer.md`      | Edit (self-check clarify + LOD input)                                        | 1d, 2f     |
| `prompts/finding-critic.md`         | Edit (LOD-aware input)                                                       | 2f         |
| `prompts/report-writer.md`          | Edit (LOD-aware input)                                                       | 2f         |
| `prompts/fix-planner.md`            | Edit (LOD output)                                                            | 2e         |
| Remaining 11 prompt files           | Edit (LOD output + incidental placeholder)                                   | 2e         |
| `templates/finding.md`              | Edit (add LOD-0, LOD-1, LOD-2 definitions)                                   | 2a         |
| `templates/agent-common.md`         | **Create** (shared LOD output + incidentals)                                 | 2b         |
| `templates/wave-report.md`          | Edit (LOD-0 table + refs)                                                    | 2d         |
| `security-analyst.md`               | Edit (FINDINGS_DIR, LOD spawning, consolidation, mapping table, wave->group) | 2c, 3a, 5b |
| `SKILL.md`                          | Edit (LOD docs, group rename, context budget, directory listing)             | 3b, 6      |
| `full.md`                           | Rewrite (slim + group rename)                                                | 3c, 4a     |
| `recon.md`                          | Rewrite (slim)                                                               | 4b         |
| `prompts/threat-model-agent.md`     | **Create**                                                                   | 5a         |
| `threat-model.md`                   | Edit (use new agent prompt)                                                  | 5a         |
| `plugins/README.md`                 | Edit (add conflict guidance)                                                 | 5b         |


**Total: 30 file edits, 2 new files created**