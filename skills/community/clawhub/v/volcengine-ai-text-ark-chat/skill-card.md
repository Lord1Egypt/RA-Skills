## Description:

Text generation and chat completion on Volcengine ARK for long-form writing, summarization, extraction, rewriting, Q&A, and prompt optimization with ARK text models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:


## Use Case:

Developers, employees, and external users use this skill to route text tasks to Volcengine ARK chat models with stable request defaults and reproducible templates. It is intended for chat, summarization, rewriting, extraction, Q&A, and prompt optimization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected prompts or text tasks may be sent to Volcengine ARK.

Mitigation: Use the skill only when the configured ARK account, region, and data-handling requirements are acceptable, and avoid submitting secrets or sensitive personal data unless approved.

Risk: The skill requires ARK_API_KEY and endpoint configuration to call the ARK chat completion API.

Mitigation: Verify credentials, endpoint ID, and region before use, and do not expose API keys in prompts, generated output, or shared logs.

## Reference(s):

- [Sources](references/sources.md)
- [Volcengine ARK Chat Completions API endpoint](https://ark.cn-beijing.volces.com/api/v3/chat/completions)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/volcengine-ai-text-ark-chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with text responses, parameter notes, and inline bash request templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include the generated or transformed text plus key ARK request parameters such as model endpoint, region, temperature, max_tokens, and top_p when used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
