## Description:

Local shell copilot for command planning, safe execution, preview-first workflows, output summarization, privacy-aware history controls, and step-by-step terminal help.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agistack](https://clawhub.ai/user/agistack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Terminal to plan, preview, execute, summarize, and review local shell commands during file inspection, debugging, and automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run arbitrary local shell commands, which may modify files, invoke network tools, or execute unsafe operations.

Mitigation: Use preview mode and review the command, working directory, and reported risk before allowing execution; require explicit confirmation for high-risk commands.

Risk: Local command and output history may contain sensitive information.

Mitigation: Use output-free logging for sensitive work and redact displayed output when commands may expose secrets.

Risk: Command risk detection and token redaction are not complete safety boundaries.

Mitigation: Manually review destructive, credential-bearing, or privilege-escalating commands instead of relying solely on automated checks.

## Reference(s):

- [Terminal Philosophy](references/philosophy.md)
- [ClawHub Terminal Skill](https://clawhub.ai/agistack/skills/terminal)
- [AGIstack Publisher Profile](https://clawhub.ai/user/agistack)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands and command-result summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local command stdout and stderr; sensitive-looking values can be redacted for display and stored history.]

## Skill Version(s):

1.0.2 (source: skill.json and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
