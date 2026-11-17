## Description:

Automates workspace tasks including summarizing recent changes, adding timestamped notes, and cleaning old log files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mmogdeveloper](https://clawhub.ai/user/mmogdeveloper)

### License/Terms of Use:


## Use Case:

Developers and workspace users use Qiuqiu Helper to summarize recent workspace changes, save timestamped notes, and remove old log files during routine workspace maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can append persistent notes and may capture sensitive information if used carelessly.

Mitigation: Require explicit confirmation before writing notes and avoid storing secrets or sensitive personal data.

Risk: The skill can delete old log files with limited scoping guidance.

Mitigation: Restrict log cleanup to a known logs directory and confirm the target path and retention period before deletion.

## Reference(s):

- [Qiuqiu Helper ClawHub skill page](https://clawhub.ai/mmogdeveloper/skills/qiuqiu-helper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text responses with proposed workspace actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append notes to files or delete old log files when the agent executes corresponding workspace actions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
