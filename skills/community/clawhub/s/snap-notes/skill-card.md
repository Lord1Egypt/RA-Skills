## Description:

AI 速记敏捷助手 helps office, sales, and procurement users capture fragmented notes, enrich them with AI quality checks, retrieve them semantically, and generate business insight summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iliubo1104-sketch](https://clawhub.ai/user/iliubo1104-sketch)

### License/Terms of Use:

MIT

## Use Case:

Employees, sales teams, and procurement teams use this skill to capture business notes, identify missing quote or requirement details, search local note history by intent, and summarize recurring customers, products, risks, and work priorities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI features can expose business notes, passwords, API keys, tokens, customer secrets, or confidential deal details to the configured model provider.

Mitigation: Do not store secrets or confidential deal details in this tool; use only a trusted HTTPS AI endpoint with a limited key.

Risk: Search and analysis can transmit stored notes to the configured AI provider.

Mitigation: Review the skill before installing and only enable AI features with an approved provider whose data handling is acceptable for the notes being processed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iliubo1104-sketch/skills/snap-notes)
- [README.md](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores notes locally as JSONL files and may call a configured OpenAI-compatible AI endpoint for enrichment, search, and analysis.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
