## Description:

Fetch and summarize Ultrahuman Ring/CGM metrics inside OpenClaw using the Ultrahuman MCP server via mcporter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devpranoy](https://clawhub.ai/user/devpranoy)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to retrieve Ultrahuman Ring or CGM metrics through an MCP server and produce short daily or weekly health summaries. It is useful for reporting sleep, steps, recovery, movement, active minutes, VO2 max, HRV, and resting heart rate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Ultrahuman credentials and sensitive health summaries.

Mitigation: Treat the Ultrahuman token and generated summaries as sensitive personal data, and avoid running the skill in environments containing unrelated secrets.

Risk: The skill relies on a third-party Ultrahuman MCP server whose version is not pinned in the artifact.

Mitigation: Use a pinned and reviewed Ultrahuman MCP server version before installing or running the skill.

Risk: Credential lookup may fall back to local OpenClaw configuration if environment variables are absent.

Mitigation: Prefer explicit environment variables for Ultrahuman credentials and review local configuration before execution.

## Reference(s):

- [Ultrahuman Developer Portal](https://vision.ultrahuman.com/developer)
- [Ultrahuman MCP repository](https://github.com/Monasterolo21/Ultrahuman-MCP)
- [ClawHub skill page](https://clawhub.ai/devpranoy/skills/ultrahuman-openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and JSON snippets, plus plain-text health summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily summaries are concise by default and may include sensitive personal health metrics.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
