---
name: skill-portfolio-audit
slug: skill-portfolio-audit
displayName: Skill Portfolio Audit
version: "1.1.9"
description: >
  Generates evidence-based portfolio audits, candidate scorecards, privacy
  classifications, consolidation plans, and a persistent execution queue with
  dependency-linked tasks for Skill portfolio management. The audit is
  read-only against existing Skills: it does not modify, delete, publish, or
  execute any original Skill; the persistent execution queue writes only to a
  separate task ledger file outside the audited Skills. Use when the user asks
  to inventory Skills, identify duplicated or stale Skills, decide which
  recurring workflows deserve standalone Skills, or assess which Skills are
  safe and valuable to share publicly.
  中文触发词: 技能组合审计, 机会评估, 重复检测, 分享价值分级
description_zh: Skill 组合审计与机会评估
description_en: Skill Portfolio Audit
not_for:
  - Designing, creating, or publishing a single Skill (use a skill-design or audit-publish skill)
  - Debugging Skill installation or platform publish failures (use a debugging skill)
  - Auditing code repositories or financial project portfolios
  - Executing or modifying any Skill listed in the audit output
agent_created: true
read_when:
  - "skill audit"
  - "portfolio review"
  - "duplicate detection"
  - "sharing classification"
  - "Skill 组合审计"
  - "机会评估"
---

# Skill Portfolio Audit

## When to use

- The user wants to inventory existing Skills, identify duplicates or stale versions.
- The user wants to find workflows worth turning into Skills from high-frequency work.
- The user needs to distinguish private Skills, config-reusable Skills, and publicly shareable Skills.
- The user needs Skill portfolio merge, split, maintenance, and publish prioritization.

## Workflow

### Step 1: [Deterministic] Define scope

1. Confirm the scan range: user-level Skills, project-level Skills, published copies, and scattered workflow scripts/docs within projects.
2. Read-only audit; do not delete, publish, or move original Skills.
3. Distinguish four asset types: installed generic Skills, self-built user-level Skills, project-level Skills, and un-encapsulated script/doc workflows.

### Step 2: [Deterministic] Inventory existing Skills

1. Enumerate all `SKILL.md` files.
2. Read frontmatter, Workflow, Hard Rules, Failure Handling, Output Format, and supporting files.
3. Record: name, path, version, enabled status, `agent_created`, dependencies, personal-data dependencies, company-data dependencies, maturity.
4. For same-name or same-function copies, compute hashes or compare versions to identify missing single-source-of-truth and version drift.

### Step 3: [LLM] Map recurring work

Aggregate high-frequency work from three evidence layers:

1. File output volume and date distribution (e.g. daily reports, analyses, layout HTML).
2. Work logs and long-term memory for sustained tasks.
3. Historical conversations for repeated requests and representative cases.

For each workflow, record: trigger, input, stable steps, variable steps, output, frequency evidence, existing Skill coverage, failure cost, sensitivity.

### Step 4: [LLM] Decide the right form

Judge in this order:

1. Only needs rules or format constraints, with clear input/output: a single Skill.
2. Multi-step sequence with checkpoints: a Workflow Skill.
3. Subtask count and path vary with materials: an Agent.
4. Low-frequency, one-off, mainly depends on ad-hoc judgment: do not Skill-ify.

Avoid stuffing everything into one God Skill. Prefer establishing orchestration Skills that reuse existing search, writing, review, layout, and publishing Skills.

### Step 5: [LLM] Score candidates

Score each 0-5:

| Dimension | Meaning |
|---|---|
| Frequency | Daily/weekly recurring gets high score |
| Stability | More stable steps and acceptance criteria = higher |
| Time saved | Saves time, reduces omissions or errors |
| Independence | Can form a clear input/output boundary |
| Transferability | Reusable across users and industries |
| Evidence accumulated | Has templates, scripts, failure cases, real outputs |
| Maintenance cost | Fragile data sources, frequently changing rules = deduction |

Total score guidance:
- 26-35: P0, design or maintain immediately.
- 20-25: P1, run a round of real-task validation first.
- 14-19: P2, keep as a module or reference doc.
- Below 14: do not Skill-ify for now.

### Step 6: [LLM] Classify sharing value

| Type | Criteria | Action |
|---|---|---|
| Public | No personal/company data; runs with config swap | Can share publicly |
| Configurable | Method is generic, but contains private paths, vendor lists, style rules, or connectors | Share after extracting `config.example` |
| Private | Core value depends on holdings, identity, internal materials, customer info, or account structure | Local use only |
| Do not publish | Contains tokens, database IDs, customer names, internal org info, or unpublished positions | Block publish, clean up first |

Sharing value also considers: whether the target audience is clear, whether existing supply is scarce, whether results are verifiable, and whether maintenance responsibility is sustainable.

### Step 7: [LLM] Produce roadmap

Output must include:

1. Current work landscape and high-frequency evidence.
2. Existing Skill asset map.
3. P0/P1/P2 candidate matrix.
4. Merge, split, retain, stop-maintaining recommendations.
5. Private/Configurable/Public sharing classification.
6. 30/60/90-day roadmap.
7. P0 risks: hardcoded credentials, personal data, company internal info, version drift.
8. Persistent execution queue: build dependency-linked tasks for all confirmed actions, so completing one P0 does not lose the remaining items.
9. After completing each item, update the execution ledger and claim the next unblocked task from the task list.

### Repo visibility (2026-10-23)

`GET /users/{name}/repos` lists **public repos only**. To classify the full inventory, call `GET /user/repos?visibility=all` authenticated, and count private repos (backups, personal archives) separately from public skill assets — never merge the two in a portfolio report.

## Hard Rules

1. Do not infer maturity from filename alone; at least read representative `SKILL.md` files.
2. Do not equate "frequently done" with "should be Skill-ified"; must check step stability and acceptance criteria.
3. Do not put personal style corpus, investment holdings, or company internal positions into a public Skill.
4. When hardcoded credentials are found, mark P0; in the report, state the location and risk only — do not reproduce the credential value.
5. Publishing and deletion are external or destructive actions, requiring separate confirmation; this audit only gives recommendations.
6. Conclusions must give evidence: file counts, version hashes, representative cases, or historical conversations.
7. At audit completion, all confirmed items must be written into a persistent task queue with dependencies; do not execute only the first item and forget the rest.
8. Task status can only be marked complete after acceptance passes; after completing each item, check and claim the next unblocked task.

## Failure Handling

| Scenario | Action |
|---|---|
| Too many Skills | Full enumeration first, then detail-audit self-built and high-frequency Skills; installed generic Skills summarized by category |
| Sub-agent or search fails | Retry and cross-validate with Glob/Read/local stats; do not stop on single failure |
| Insufficient conversation recall | Use project logs, output file counts, and representative files as supplementary evidence; note evidence boundaries |
| A candidate has malformed or missing frontmatter (unparseable YAML or no SKILL.md) | Record the file path and the parse error as a P0 data-quality finding; do not guess its metadata and exclude it from scoring until fixed |
| Same-name copies with different content | Flag version drift; recommend setting one authoritative source and one-way publish flow |
| Personal data mixed with generic method | Split into public engine + private config/data layer |

## Output Format

```markdown
# Skill Portfolio and High-Frequency Work Audit

## Conclusion
## Current Work Landscape
## Existing Skill Assets
## Candidate Scorecard Matrix
## Merge and Split Recommendations
## Sharing Value Classification
## 30/60/90-Day Roadmap
## P0 Risks and Immediate Actions
## Evidence and Boundaries
```

## Pitfalls

- Giving a roadmap without building a task queue makes it easy to lose remaining items after completing the first P0. Audit delivery must include tasks, dependencies, status, and next-item claim rules.
- Setting all P0s to in-progress simultaneously widens the work surface. Default: only one main task in progress; others stay pending with dependency management.

## Verification

- [ ] Covered user-level, project-level, and published copies.
- [ ] Each P0 candidate has frequency and real-output evidence.
- [ ] Distinguished Skill, Workflow Skill, Agent, and do-not-Skill-ify.
- [ ] Checked for credentials, personal data, company internal data, and external publish risk.
- [ ] Identified same-name copies and version drift.
- [ ] Recommendations can be acted on: retain, merge, split, private, or publish.
