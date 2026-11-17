## Description:

Provides a reusable four-step streaming AI retrieval Q&A interaction pattern for knowledge-base products, including intent understanding, content retrieval, streamed generation, and source marking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product engineers use this skill to add transparent, streaming AI Q&A flows to knowledge-base, customer-support, education, healthcare, legal, finance, government, and enterprise assistant products. It helps structure UI states, prompts, source attribution, and React implementation patterns for retrieval-augmented answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Frontend streaming examples can expose provider API keys and user messages if copied directly into browser code.

Mitigation: Use a backend or serverless route for provider credentials, restrict upstream endpoints, and avoid sending unnecessary sensitive content.

Risk: Medical, legal, financial, or internal business deployments may produce high-impact answers or process sensitive prompts.

Mitigation: Review before production use, add domain-appropriate disclaimers, redact sensitive prompts where possible, and disclose third-party AI processing to users.

Risk: The UI and prompt examples are primarily Chinese-language and may not fit all deployment audiences.

Mitigation: Localize prompts, labels, source formats, and disclaimers before using the pattern in non-Chinese-language deployments.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zmy1006-sudo/skills/stream-ai-answer)
- [Frontend implementation reference](artifact/references/frontend-pattern.md)
- [Streaming AI prompt templates](artifact/references/prompts.md)
- [AIAnalysisCard React component](artifact/assets/AIAnalysisCard.tsx)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with TypeScript/TSX code examples and prompt/configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to be adapted by developers for their own LLM provider, retrieval source, UI framework, and domain-specific disclaimer requirements.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
