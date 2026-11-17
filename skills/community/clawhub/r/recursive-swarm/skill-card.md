## Description:

Bounded recursive orchestration for complex tasks that are too large for one agent turn but cleanly decompose into a few independent subproblems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plgonzalezrx8](https://clawhub.ai/user/plgonzalezrx8)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to decompose complex research, audit, coding, ops, or synthesis tasks into a bounded task tree with explicit state, saved artifacts, merge points, and audit events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scripts can write outside the intended run folder when given crafted paths or custom output locations.

Mitigation: Review before installation, use trusted task inputs, keep runs in a dedicated directory, avoid custom --out paths outside the run folder, and use simple dotted node IDs such as 1.2.

Risk: Task summaries, notes, and results are persisted in local run artifacts.

Mitigation: Avoid using the skill on sensitive exports unless local artifact persistence is acceptable.

## Reference(s):

- [Recursive Swarm skill page](https://clawhub.ai/plgonzalezrx8/skills/recursive-swarm)
- [Example run](references/example-run.md)
- [Quiet child execution pattern](references/quiet-mode.md)
- [Recursive-swarm run tree schema](references/tree-schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON run artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local run directories containing tree.json, events.jsonl, summary.md, node specs, notes, and results.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
