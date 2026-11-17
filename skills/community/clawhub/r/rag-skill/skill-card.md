## Description:

rag-skill queries a Prana-hosted RagFlow knowledge base for RAG-related content, including technology-and-art artist profile material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaochengzhen](https://clawhub.ai/user/xiaochengzhen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit a natural-language question to a remote knowledge-base agent and receive RAG-related answers from the configured RagFlow collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API key handling is flagged as unsafe.

Mitigation: Inject PRANA_SKILL_API_FLAG through a temporary environment or managed secret mechanism when practical, and do not print or paste the value in terminal output.

Risk: The skill declares a purchase-history endpoint that is unrelated to normal knowledge-base querying.

Mitigation: Do not call the purchase-history endpoint unless the user explicitly asks for account, purchase, or request-history information.

Risk: Remote knowledge-base queries may send user-provided text to the Prana service.

Mitigation: Use the skill only for non-sensitive knowledge-base questions and avoid including credentials, payment details, or personal data in the question.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaochengzhen/skills/rag-skill)
- [Publisher profile](https://clawhub.ai/user/xiaochengzhen)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON service responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PRANA_SKILL_API_FLAG for remote API calls; the question parameter should come from user input and should avoid sensitive data.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
