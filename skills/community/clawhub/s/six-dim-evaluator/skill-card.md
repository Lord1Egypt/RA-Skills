## Description:

Evaluates agent skills across six dimensions (T/C/O/E/M/U), compares versions, and produces scores with improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pagoda111king](https://clawhub.ai/user/pagoda111king)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to assess ClawHub-style agent skills, compare score changes between versions, and identify improvement actions before release or maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests write and shell execution authority while evaluating other skill directories.

Mitigation: Install only after review, limit use to read-only evaluation when possible, and grant write or shell execution only when tests or generated files are explicitly required.

Risk: The skill description mentions log analysis and stored evaluation data without clear storage, retention, or deletion controls.

Mitigation: Avoid pointing it at private logs or sensitive skill data until the publisher documents data handling, retention, deletion, and dependency-update practices.

Risk: Server security evidence marks the release as suspicious because the requested authorities are broader than the documented controls.

Mitigation: Review the source and scan results before deployment, constrain the workspace it can access, and run it in a sandboxed environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pagoda111king/skills/six-dim-evaluator)
- [Publisher profile](https://clawhub.ai/user/pagoda111king)
- [Six Dim Evaluator documentation](https://docs.cloud-shrimp.com/six-dim-evaluator)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, code, shell commands, guidance]

**Output Format:** [Markdown or JSON evaluation results with scores, comparisons, and improvement suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated reports, score summaries, and suggested follow-up actions.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter, package.json, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
