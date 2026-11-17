## Description:

Validate Agent provides agent validation and quality-assurance guidance to reduce silent system errors and produce reproducible evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jack123255829](https://clawhub.ai/user/jack123255829)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to prompt validation before task completion, after fixes, before important answers, and when tracking cross-session commitments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run often and add validation overhead to routine agent work.

Mitigation: Review or narrow the trigger language when the skill should apply only to higher-risk tasks.

Risk: Cross-session commitment tracking may create a simple promises.md file.

Mitigation: Review generated tracking files and remove or limit them when persistent commitment records are not desired.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown/plain-text guidance with checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May add validation overhead and may create a simple promises.md tracking file for cross-session commitments.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
