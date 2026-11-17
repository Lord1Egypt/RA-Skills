## Description:

Self-Prompt helps automated jobs trigger real OpenClaw agent turns and relay the resulting responses back to a chat target.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eliranwong](https://clawhub.ai/user/eliranwong)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to make scheduled jobs, monitoring alerts, accountability checks, and research tasks receive an agent response instead of being treated as background chat messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated agent responses may be reposted to a chat target without enough human review.

Mitigation: Use only with trusted agents and trusted chat targets, and add approval or filtering before automated responses are posted to a group.

Risk: Task messages or agent responses can include sensitive information that is reposted or logged.

Mitigation: Avoid secrets, credentials, personal data, private business data, and sensitive trading details; harden or disable response logging where needed.

Risk: The helper scripts depend on the configured OpenClaw executable path.

Mitigation: Validate the OpenClaw binary path before use and set OPENCLAW_PATH to an approved executable in managed environments.

## Reference(s):

- [ClawHub skill page: Self-Prompt](https://clawhub.ai/eliranwong/skills/self-prompt)
- [ClawHub publisher profile: eliranwong](https://clawhub.ai/user/eliranwong)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Bash and Python examples plus helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper scripts accept an agent ID, group or target ID, task message, timeout, and channel.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
