## Description:

Run multi-model AI synthesis inquiries via QuorumAI. Four AI models (Claude, GPT, Gemini, Grok) compete to answer your question from specialized perspectives, get scored by an arbiter, and the best elements are synthesized into one ultimate answer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shokatma-oss](https://clawhub.ai/user/shokatma-oss)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to ask QuorumAI a question once and receive a synthesized answer from multiple model perspectives, with optional domain academies for clinical, business, technical, investment, or general inquiries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied question text may be inserted into shell-based curl examples unsafely, allowing crafted input to affect local command execution.

Mitigation: Review generated commands before execution and prefer a structured HTTP client or JSON serializer for request bodies before using arbitrary user text.

Risk: Questions and results are sent to QuorumAI and may produce a public result link.

Mitigation: Use the skill only for questions the user is willing to send to QuorumAI and share through the returned link.

Risk: The skill requires a bearer API key.

Mitigation: Keep QUORUMAI_API_KEY in the agent environment or configuration and never echo or include it in user-facing responses.

## Reference(s):

- [ClawHub QuorumAI Skill](https://clawhub.ai/shokatma-oss/skills/quorumai)
- [QuorumAI Homepage](https://quorumai.io)
- [QuorumAI API Endpoint](https://quorumai.io/api/v1/inquiry)
- [QuorumAI Account and API Keys](https://quorumai.io/account)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash curl examples and JSON API response fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QUORUMAI_API_KEY and curl; QuorumAI responses may include a public share_url.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
