## Description:

御知库 is a personal knowledge-base skill that stores Markdown, PDF, and text documents, searches them by keyword or simple semantic matching, and helps agents answer from local knowledge first.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zton100](https://clawhub.ai/user/zton100)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users can use this skill to maintain a local personal knowledge base and retrieve relevant stored material when answering knowledge-oriented questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Imported documents may be stored as full plaintext content under ~/.yuzhi.

Mitigation: Review files before adding them and avoid importing secrets, credentials, agent configuration, logs, or broad workspace files.

Risk: Broad trigger language may cause the skill to be used for general knowledge questions where local retrieval is not intended.

Mitigation: Prefer explicit knowledge-base lookup commands and verify retrieved snippets before relying on them in an answer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zton100/skills/yuzhi)
- [ClawHub publisher profile](https://clawhub.ai/user/zton100)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown or plain text with CLI commands and retrieved document snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference locally stored knowledge-base entries from ~/.yuzhi when available.]

## Skill Version(s):

1.0.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
