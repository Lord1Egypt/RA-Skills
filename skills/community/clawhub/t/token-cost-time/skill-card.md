## Description:

Estimate LLM task token usage, cost, and duration using rule-based classification and optional local profile data without external dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[highnoonoffice](https://clawhub.ai/user/highnoonoffice)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to estimate LLM task token usage, cost, and duration, compare models, and record completed runs for local calibration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local profile and execution log files may contain sensitive objective text or proprietary task details.

Mitigation: Avoid recording sensitive objectives or proprietary task details in local calibration data, especially when those files may be shared or backed up.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/highnoonoffice/skills/token-cost-time)
- [Project homepage](https://github.com/highnoonoffice/hno-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces estimates and model comparisons; optional local profile and execution log data can calibrate future estimates.]

## Skill Version(s):

0.1.4 (source: release evidence; artifact frontmatter lists 0.1.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
