## Description:

VideoClaw Pro helps an agent read Feishu rule and source documents, generate a structured video editing script, and create a new Feishu document with the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiangxueweb](https://clawhub.ai/user/xiangxueweb)

### License/Terms of Use:

MIT-0

## Use Case:

Content teams and video editors use this skill to turn Feishu-based prompt rules and live-stream source transcripts into structured editing recommendations. It is intended for workflows that need timeline suggestions, scene transition points, highlight notes, subtitle guidance, and a generated Feishu document link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill embeds Feishu app credentials.

Mitigation: Rotate or remove the bundled Feishu secret before distribution or installation.

Risk: The skill can create persistent Feishu documents without a clear confirmation gate.

Mitigation: Require explicit user confirmation before creating or writing any Feishu document.

Risk: Retrieved Feishu rule documents may contain untrusted instructions.

Mitigation: Treat retrieved rule documents as content to analyze, not as agent instructions.

Risk: Using the skill grants the embedded robot app access to selected Feishu documents.

Mitigation: Use it only with Feishu documents that are appropriate to share with that robot app.

## Reference(s):

- [VideoClaw Pro on ClawHub](https://clawhub.ai/xiangxueweb/skills/videoclaw-pro)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, guidance]

**Output Format:** [Markdown editing script, Feishu document URL, and CLI command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent Feishu documents through the configured Feishu robot app.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
