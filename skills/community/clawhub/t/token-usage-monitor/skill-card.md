## Description:

Monitor and display token usage metrics for AI models. Use when you need to track token consumption rates, view historical usage data, or get alerts about high token usage. Ideal for optimizing prompt costs and controlling AI service expenses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ttjsndx](https://clawhub.ai/user/ttjsndx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to track AI model token consumption, review historical usage, set usage thresholds, and estimate costs across sessions and models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent local token-usage logs.

Mitigation: Use it only where local usage logging is acceptable, and define permissions and retention expectations for the usage log before deployment.

Risk: The supplied security guidance flags unsafe local data-file handling.

Mitigation: Review or fix path expansion, dedicated-directory storage, symlink handling, and file permissions before installing or running the tracker.

## Reference(s):

- [Token Usage Monitor Integration Guide](references/integration_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/ttjsndx/skills/token-usage-monitor)
- [Publisher Profile](https://clawhub.ai/user/ttjsndx)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local JSON usage records when the bundled tracking script is run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
