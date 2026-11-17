## Description:

Capture and promote durable agent learnings in QMD-indexed Markdown when reflection or reusable memory is requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shakerg](https://clawhub.ai/user/shakerg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to turn intentional reflection, recurring failures, and accepted conventions into concise, reviewable Markdown knowledge while preserving existing workspace conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable Markdown capture can preserve incorrect, sensitive, or unnecessary information if a proposed learning is accepted without review.

Mitigation: Review the proposed learning, evidence, classification, and destination before approval, and redact secrets, personal data, raw prompts, and irrelevant command output.

Risk: QMD collection or embedding commands can index unintended directories if configured too broadly.

Mitigation: Keep QMD collections limited to intended Markdown paths and run update or embedding commands only when they match the workspace's approved setup.

Risk: Optional tools such as QMD add dependency and installation risk.

Mitigation: Prefer pinned or reviewed versions of optional tools and rely on the host agent's normal authorization model before executing setup or indexing commands.

## Reference(s):

- [QMD Learning Loop homepage](https://github.com/shakerg/qmd-learning-loop)
- [QMD project](https://github.com/tobi/qmd)
- [Destination Discovery](references/destination-discovery.md)
- [Evaluation Cases](references/evaluation-cases.md)
- [QMD Workflow](references/qmd-workflow.md)
- [Review Loop](references/review-loop.md)
- [Templates](references/templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with proposed file changes, optional shell command blocks, and concise status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update existing Markdown destinations only after user approval; QMD indexing commands are optional and depend on the workspace setup.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
