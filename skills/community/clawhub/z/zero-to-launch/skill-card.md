## Description:

Zero-to-Launch helps independent developers, founders, and makers turn rough product ideas into a clear launch plan through guided product discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viliawang-pm](https://clawhub.ai/user/viliawang-pm)

### License/Terms of Use:

MIT-0

## Use Case:

External founders, product managers, makers, and independent developers use this skill to clarify early product ideas, explore users and market opportunity, compare alternatives, define validation steps, and scope an MVP. It is intended for product ideation and launch planning conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes unrelated WeChat publishing utilities with committed API credentials and draft-creation capability.

Mitigation: Rotate the exposed WeChat secret, remove committed config.json, and exclude the WeChat publisher directory before installing or redistributing the skill.

Risk: The included preview tooling can render HTML content locally.

Mitigation: Avoid previewing untrusted HTML and review local preview files before opening them in a browser.

Risk: Product planning output may be incomplete, speculative, or based on user-provided assumptions.

Mitigation: Treat the generated launch plan as decision support and validate recommendations with real users, market research, and human review before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/viliawang-pm/skills/zero-to-launch)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown conversation responses with ASCII diagrams, structured tables, and launch-planning templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces iterative product discovery artifacts such as personas, competitive matrices, validation plans, MVP scope, prototype sketches, and a one-page PRD.]

## Skill Version(s):

3.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
