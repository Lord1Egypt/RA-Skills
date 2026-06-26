## Description: <br>
Provides a reusable Chinese-language pattern for building streaming AI retrieval-and-answer interfaces with visible analysis steps, source display, and domain prompt templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to add a streaming RAG-style answer experience to React, H5/WebApp, enterprise knowledge base, customer support, consulting, or domain education products. It is especially suited to interfaces that need visible intent analysis, retrieval progress, generated answers, source links, and clear disclaimers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The examples include streaming LLM API usage that requires sensitive provider credentials. <br>
Mitigation: Keep API keys on the server and call the provider through an application backend rather than exposing credentials in client code. <br>
Risk: The skill targets medical, legal, financial, government, and other high-stakes knowledge-base scenarios where generated answers can be misleading or jurisdiction-sensitive. <br>
Mitigation: Review prompts, disclaimers, citation rules, and domain policy requirements before production use, and require qualified human review for high-stakes advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zmy1006-sudo/stream-ai-answer) <br>
- [Frontend implementation pattern](references/frontend-pattern.md) <br>
- [Streaming AI prompt templates](references/prompts.md) <br>
- [React analysis card component](assets/AIAnalysisCard.tsx) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript/TSX component code, prompt templates, and streaming API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes source parsing, disclaimer display, streaming response handling examples, and step-status UI patterns. Provider API keys should stay server-side.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
