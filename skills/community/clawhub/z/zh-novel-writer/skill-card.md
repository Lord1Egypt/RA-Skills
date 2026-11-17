## Description:

Generates batches of Chinese web-novel chapters from an outline by prompting configured external LLM APIs and saving chapter Markdown files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shine8592](https://clawhub.ai/user/shine8592)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to batch-generate Chinese web-novel chapters from a JSON outline, chapter range, and configured API credentials. It is intended for draft generation rather than single-chapter polish, human editorial review, or publication-grade proofreading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outlines, manuscript excerpts, and generated chapter text can be sent to ModelScope, Fyra, or Ph8 when API keys are configured.

Mitigation: Avoid sending sensitive or confidential manuscript material, review the selected provider's data terms, and use dedicated API keys with spending limits.

Risk: Batch generation can continue making paid API calls across broad chapter ranges without a clear per-chapter cost limit.

Mitigation: Start with a small chapter range, monitor provider billing and logs, and run the script in a contained environment with constrained credentials.

## Reference(s):

- [API configuration](references/api-config.md)
- [Prompt template](references/prompt-template.md)
- [ModelScope chat completions endpoint](https://api-inference.modelscope.cn/v1/chat/completions)
- [Fyra chat completions endpoint](https://Fyra.im/v1/chat/completions)
- [Ph8 chat completions endpoint](https://ph8.co/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown chapter files with concise shell and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce one Markdown file per generated chapter across a requested chapter range; generated text is sent to configured external LLM APIs.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
