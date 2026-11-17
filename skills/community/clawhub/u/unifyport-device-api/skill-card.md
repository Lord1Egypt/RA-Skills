## Description:

Explain and safely call the public UnifyPort Device API for workspaces, provider accounts, authentication, runtime, messages, conversations, contacts, groups, API keys, webhooks, provider regions, and standard events. Use for UnifyPort API documentation, request preparation, provider capability questions, error interpretation, or an explicitly requested allowlisted live operation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unifyport](https://clawhub.ai/user/unifyport)

### License/Terms of Use:

MIT-0

## Use Case:

Developers integrating UnifyPort can use this skill to understand supported API operations, prepare requests and examples, assess provider capabilities, interpret errors, and make allowlisted live calls when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live API use can expose sensitive account or conversation data or cause external state changes.

Mitigation: Use a limited API key, make live calls only when explicitly requested, confirm sensitive changes, and redact returned data.

Risk: Credentials or webhook signing secrets could be exposed through prompts or output.

Mitigation: Keep secrets out of chat and ordinary output; use controlled input and suppress secret values.

## Reference(s):

- [UnifyPort API documentation](https://www.unifyport.ai/docs/#introduction)
- [Provider message support](https://www.unifyport.ai/docs/provider-guide/provider-message-support/)
- [Provider actions support](https://www.unifyport.ai/docs/provider-guide/provider-actions-support/)
- [Simplified Chinese API documentation](https://www.unifyport.ai/zh-CN/docs/#introduction)
- [UnifyPort Device API release page](https://clawhub.ai/unifyport/skills/unifyport-device-api)
- [Safety guidance](artifact/references/en/safety.md)
- [Operation catalog](artifact/references/operations.json)
- [Standard event catalog](artifact/references/events.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Code, JSON, Shell commands]

**Output Format:** [Markdown guidance with JSON request examples, code snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live calls use documented allowlisted actions; sensitive values and returned data are handled with the skill's stated safeguards.]

## Skill Version(s):

1.1.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
