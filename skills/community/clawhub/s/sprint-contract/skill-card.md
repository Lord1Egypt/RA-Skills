## Description:

Sprint Contract is a multi-agent development workflow that uses explicit completion criteria and independent QA evaluation for feature builds, complex bug fixes, and code reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrpixelraf](https://clawhub.ai/user/mrpixelraf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use Sprint Contract to plan, execute, and independently evaluate medium or complex development tasks with explicit completion criteria, file-based handoffs, and a QA decision gate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The trigger description is broad, so the skill may be invoked for many coding tasks where multi-agent coordination adds overhead.

Mitigation: Use it deliberately for medium or complex development work where a separate builder and evaluator are worth the added coordination.

## Reference(s):

- [Sprint Contract Examples](references/contract-examples.md)
- [Anthropic harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- [Sprint Contract on ClawHub](https://clawhub.ai/mrpixelraf/skills/sprint-contract)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown instructions, checklists, and evaluator prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce BRIEF.md and HANDOFF.md workflow artifacts when applied by an agent.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
