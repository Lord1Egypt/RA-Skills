---
name: skill-enhance
description: Create, improve, review, and locally customize skills with a quality-first workflow. Use this skill when the user wants to build a new skill, strengthen an existing one, improve trigger accuracy or execution clarity, fill missing artifacts such as README, evals, metadata, or references, review publish readiness, or safely modify a locally available skill package. When local modification is requested, verify access and writeability first, report blockers clearly, and confirm the target path and edit intent before editing. Do not use it for ordinary prose editing, unrelated code refactors, or simple skill discovery or installation.
---

# Skill Enhance

Use this skill to produce high-quality skills that are not only structurally valid, but also clear, triggerable, executable, testable, and publishable.

This skill is intentionally heavier than a lightweight skill scaffolder. Favor quality over speed when the user is creating or enhancing a skill that other agents or users will depend on.

## Trigger Boundary

Use this skill when the task is primarily about skill quality, including:

- creating a new skill from scratch
- enhancing an existing skill
- improving a locally stored or installed skill
- improving skill trigger accuracy
- strengthening a skill's output contract
- adding or refining README, evals, references, metadata, or release notes
- reviewing whether a skill can reliably guide an LLM
- checking whether a skill is ready to publish

Do not use this skill as the main path for:

- ordinary prose editing unrelated to skills
- general code refactoring unrelated to skills
- simple skill discovery or installation
- platform-specific publishing steps that do not affect the skill package itself

If the request is mixed, use this skill only for the skill-quality slice.

## Core Principle

Do not stop at "here is a draft."
The goal is to deliver a skill package or a concrete enhancement plan that closes the gap between:

- a loosely defined skill idea
- and a dependable skill another LLM can actually use well

Treat these as first-class quality dimensions:

1. trigger quality
2. execution clarity
3. output contract quality
4. artifact completeness
5. validation coverage
6. publish readiness
7. local edit safety

## Canonical Workflow

`SKILL.md` is the source of truth for the workflow.
`README.md` should keep only a concise human-facing summary.
`references/workflows.md` should extend or explain the workflow, but should not redefine it as a competing source.

Unless the user requests a lighter path, run this workflow in order:

### Phase 1: Identify mode

Decide whether the task is:

- new skill creation
- existing skill enhancement
- local skill modification
- trigger optimization
- artifact completion
- quality review
- publish-readiness review

## Mode Selection Rule

Choose the primary mode using this priority:

1. If the user wants to change a locally available skill package, use **Local skill modification**.
2. If the user asks whether a skill is ready for release or what is still missing before release, use **Publish-readiness review**.
3. If the user mainly wants to improve when the skill triggers or stops triggering, use **Trigger optimization**.
4. If the user mainly wants to add or fix missing files such as README, evals, metadata, or references, use **Artifact completion**.
5. If the user already has a skill and wants broader quality improvements, use **Existing skill enhancement**.
6. If the user wants a new skill from scratch, use **New skill creation**.
7. If the request is mostly diagnostic and no concrete package changes are yet requested, use **Quality review**.

If several modes apply, pick the highest-priority primary mode and treat the others as supporting concerns.

### Phase 2: Check local editability when relevant

If the task involves a local skill package:

- identify the target skill
- identify or confirm the target path
- determine whether the environment can access the path
- determine whether the environment can write to the path
- determine whether the user wants analysis only or actual edits

### Phase 3: Define the contract

Lock down:

- skill purpose
- positive trigger cases
- negative trigger cases
- output contract
- required artifacts
- validation expectations

### Phase 4: Build or revise artifacts

Create or update the package files that are required for the current goal.

### Phase 5: Run review gates

Always review:

- trigger boundary
- output contract
- execution reliability
- artifact completeness
- publish readiness

Also review local modification safety when the target is a local installed skill.

### Phase 6: Report status

State:

- what was changed
- what still needs work
- whether the package is draft, internally usable, release-candidate, or publish-ready

## Canonical Package Layout

Use this as the default package layout for a reusable skill:

```text
skill-name/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── evals/
│   └── evals.json
└── references/
    ├── trigger-design.md
    ├── output-contracts.md
    ├── review-checklist.md
    ├── publish-readiness.md
    ├── artifact-matrix.md
    ├── skill-packaging.md
    ├── workflows.md
    └── package-layout.md
```

Interpretation:

- `SKILL.md`: required
- `README.md`: strongly recommended for reusable or published skills
- `agents/openai.yaml`: recommended metadata entry point
- `evals/evals.json`: strongly recommended when the skill should be reviewable
- `references/`: selected support docs, not a dump of unrelated material

If the skill is only a tiny local experiment, the package may be lighter, but reusable skills should default to this structure.

## Task Modes

Classify the request into one primary mode:

1. **New skill creation**
2. **Existing skill enhancement**
3. **Local skill modification**
4. **Trigger optimization**
5. **Artifact completion**
6. **Quality review**
7. **Publish-readiness review**

If several modes are present, use this sequence:

1. summarize the current state and target
2. identify the quality gaps
3. decide what the skill must do and when it should trigger
4. if local modification is requested, verify access and confirm the target path
5. define or rewrite the output contract
6. produce or revise the package artifacts
7. run the review gates
8. state whether the skill is publish-ready

## Workflow

### 1. Capture the real objective

Before writing anything, determine:

- is the user creating a new skill or enhancing an existing one
- is the user asking to modify a local skill package
- who the skill is for
- what user requests should trigger it
- what the skill must produce when triggered
- whether the target is project-local, shareable, or release-ready

If an existing skill already exists, read it first and extract:

- current capability
- current trigger wording
- bundled artifacts
- gaps or inconsistencies

### 1.5 Check local editability before modifying an existing local skill

If the request involves changing a locally available skill, do not jump straight into edits.

First determine:

- whether the target skill path is known
- whether the current environment can access that path
- whether the current environment can write to that path
- whether the user is asking for analysis only or actual modification

If the path is unclear, ask the user to confirm the target path or clearly identify the skill.

If the path is known but the environment cannot modify it, say so clearly and stop short of claiming the change can be applied.

If the path is writable, confirm the target path and edit intent before making changes.

Treat these as separate states:

- **analyzable but not editable**
- **editable after confirmation**
- **ready to modify now**

### 1.6 Local modification decision table

Use this decision table whenever the target is a local skill package:

- **If the target path is unknown**: ask the user to identify or confirm the path before planning edits.
- **If the target path is known but the environment cannot access it**: explain that the skill can review the request conceptually but cannot inspect or modify that package from the current environment.
- **If the target path is accessible but not writable**: stay in analysis mode, describe the recommended changes, and say clearly that edits cannot be applied from the current environment.
- **If the target path is writable but the user has not confirmed edit intent**: summarize the planned changes and ask for confirmation before editing.
- **If the target path is writable and the user has confirmed edit intent**: apply the changes and report exactly what was modified.

## Mode-Specific Playbooks

### Playbook A: New skill creation

Use this when the user wants a new skill.

1. Identify the target capability and audience.
2. Define trigger boundary and output contract.
3. Create the canonical package layout.
4. Write `SKILL.md` first, then supporting artifacts.
5. Add eval prompts.
6. Run review gates and report readiness.

### Playbook B: Existing skill enhancement

Use this when the user already has a skill package.

1. Read the current package first.
2. Identify capability gaps, trigger problems, artifact gaps, and unclear instructions.
3. Decide which files need revision.
4. Apply targeted improvements instead of rewriting blindly.
5. Re-run review gates and summarize what improved.

### Playbook C: Local skill modification

Use this when the target skill exists on the local machine.

1. Identify the target skill and path.
2. Check accessibility and writeability.
3. Apply the local modification decision table.
4. If the path is not writable, stay in analysis mode and say so clearly.
5. If the path is writable, confirm the edit intent before changing files.
6. Apply changes only after confirmation.
7. Report exactly what was changed in the local package.

### Playbook D: Publish-readiness review

Use this when the user wants release confidence.

1. Review package naming and description quality.
2. Review README, metadata, evals, and references.
3. Review trigger boundary and output contract.
4. Review whether the package is understandable to a new user.
5. Report readiness level and the remaining gaps.

### 2. Define the skill contract

Do not write `SKILL.md` before the contract is clear.

At minimum, define:

- the skill's purpose
- positive trigger cases
- negative trigger cases
- expected output structure
- required artifacts
- validation expectations

Use `references/trigger-design.md` and `references/output-contracts.md`.
Use `references/workflows.md` and `references/package-layout.md` when the user needs a fixed process or a standard file tree.

### 3. Build or revise the package

By default, a strong skill package should include:

- `SKILL.md`
- `README.md`
- `agents/openai.yaml`
- `evals/evals.json`
- relevant `references/`

Use `references/artifact-matrix.md` to decide which artifacts are required and which are optional.

Do not assume a valid `SKILL.md` alone is enough for a publish-quality skill.

### 4. Strengthen trigger quality

Review the trigger description for:

- under-triggering
- over-triggering
- ambiguous phrasing
- missing common request patterns
- missing exclusions

If needed, rewrite the description so the skill is more likely to trigger when useful, but less likely to hijack unrelated tasks.

### 5. Strengthen execution reliability

Check whether the skill instructions are actually actionable.

Specifically review:

- whether the workflow is clear
- whether decision points are explicit
- whether outputs are well specified
- whether the skill asks for real deliverables, not just abstract advice
- whether references are discoverable and scoped correctly

Use `references/review-checklist.md`.

### 6. Add validation coverage

Create realistic eval prompts whenever the skill is expected to produce repeatable, reviewable outputs.

Use `evals/evals.json` to cover:

- core happy-path creation or enhancement
- trigger-boundary cases
- artifact-completion cases
- publish-readiness cases
- at least one non-trigger or out-of-scope case

If the skill is subjective, the evals can still define expected output qualities rather than strict assertions.

### 7. Review publish readiness

Use `references/publish-readiness.md` and `references/skill-packaging.md`.

Before calling the work done, check:

- does the skill name make sense publicly
- does the description help discovery
- are human-facing docs separate from agent-facing instructions
- are bundled artifacts sufficient
- is the skill understandable without extra hidden context
- is there enough validation material for release review

State clearly whether the skill is:

- draft
- internally usable
- release-candidate
- publish-ready

### 8. Handle local-skill modification safely

When the target is a local skill package, explicitly report:

- the target skill name
- the target path
- whether the path was user-provided or inferred
- whether the environment can edit it
- whether user confirmation was received before edits

Never silently modify a local installed skill on assumption alone.

## Output Contract

Default to this structure unless the user requests another format:

### 1. Task mode

State whether this is new creation, enhancement, local skill modification, trigger optimization, artifact completion, quality review, or publish-readiness review.

### 2. Current-state summary

Describe the current package or the requested target in 2-4 lines.

### 3. Local target status

If a local skill is involved, state:

- target skill
- target path
- whether the path is confirmed
- whether the environment appears able to modify it
- whether user confirmation is still required
If no local skill is involved, say that this section is not applicable.

### 4. Key quality gaps or design goals

List the highest-impact issues or goals.

### 5. Recommended changes

Describe what to create, rewrite, or add.

### 6. Artifact plan

State which files are required, optional, missing, or already strong.

### 7. Review findings

Summarize trigger quality, execution reliability, output-contract quality, and publish-readiness findings.

### 8. Validation

State what was validated, what still needs validation, and whether the package is publish-ready.

## Quality Gates

The skill must explicitly check these gates when relevant:

### Trigger Boundary Review

Check whether:

- the description contains concrete usage contexts
- the skill would likely trigger when useful
- the skill excludes obvious false positives
- the trigger boundary is neither too broad nor too narrow

### Output Contract Review

Check whether:

- the skill tells the agent what to produce
- output structure is explicit
- required content is clear
- execution steps are not vague or purely advisory

### LLM Reliability Review

Check whether:

- the instructions are actionable
- the workflow has clear transitions
- important decisions are surfaced
- the skill drives toward delivery, not endless analysis

### Artifact Completeness Check

Check whether the package needs:

- `README.md`
- `agents/openai.yaml`
- `evals/evals.json`
- key references
- release notes or changelog copy

### Publish-Readiness Check

Check whether the package is understandable, verifiable, and suitable for public or team-wide use.

### Local Modification Check

Check whether:

- the target local skill is clearly identified
- the path is known or confirmed
- the environment appears able to edit it
- the user has confirmed the path and edit intent before modification
- the response clearly distinguishes analysis from applied edits

## Constraints

- Do not treat a valid frontmatter block as proof of a good skill.
- Do not produce a skill that only contains abstract theory.
- Do not skip trigger-boundary review when the skill is meant to be reused.
- Do not skip artifact completion if the user is aiming for release.
- Do not force heavyweight benchmarking when lightweight validation is enough.
- Do not claim publish readiness without checking docs, evals, and packaging materials.
- Do not claim a local skill was modified unless the target path was accessible and the user confirmed the edit.
- Do not infer write access from mere path existence.
- Do not silently edit a downloaded or installed local skill without path confirmation.

## References

- `references/trigger-design.md`: how to design strong trigger boundaries
- `references/output-contracts.md`: how to define reliable skill outputs
- `references/review-checklist.md`: quality review checklist for skill reliability
- `references/publish-readiness.md`: release-oriented review criteria
- `references/artifact-matrix.md`: which artifacts are required or optional
- `references/skill-packaging.md`: packaging guidance for local, Git, and release contexts
- `references/workflows.md`: fixed process for create, enhance, modify, and release-review tasks
- `references/package-layout.md`: canonical skill package layout and file responsibilities
