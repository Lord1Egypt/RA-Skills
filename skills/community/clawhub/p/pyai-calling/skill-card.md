## Description:

Make user-approved phone calls with the PyAI CLI, check call status, and retrieve available summaries or transcripts. Use when the user explicitly asks to call someone through their PyAI project. Requires PyAI CLI, account access, calling permissions, an owned number and credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atomsai](https://clawhub.ai/user/atomsai)

### License/Terms of Use:

MIT-0

## Use Case:

A user uses the PyAI CLI to place an explicitly authorized phone call through their project, check its status, and retrieve available call summaries or transcripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A real call can spend project credits and contact the wrong recipient if call details are incorrect.

Mitigation: Before execution, show and confirm the recipient, caller number, agent, purpose, and duration limit; obtain authorization for the real call.

Risk: Recipient details and conversation content pass through PyAI, and returned transcripts may contain sensitive information.

Mitigation: Retrieve summaries or transcripts only when available and authorized, and protect the returned content.

Risk: An unverified installation source could install an unintended CLI package.

Mitigation: Confirm the Homebrew source with PyAI before installation.

## Reference(s):

- [PyAI CLI setup](https://pyai.com/cli)
- [PyAI speech calling guide](https://pyai.com/agents/speech-calling.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text, Markdown]

**Output Format:** [Markdown with shell commands and available call status, summaries, or transcripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Call requests use a bounded duration; summaries and transcripts are available only when returned and authorized.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
