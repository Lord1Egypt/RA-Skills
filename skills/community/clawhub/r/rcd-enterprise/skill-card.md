## Description:

通过关键词和分类查询企业信息；包含企业基本信息、股东、高管等34个分类。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xinxin970620-prog](https://clawhub.ai/user/xinxin970620-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up Chinese enterprise records by company keyword and requested information category, such as basic registration details, shareholders, executives, change records, risks, mortgages, penalties, annual reports, and historical data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed because the skill documents command-line and chat-style API_KEY handling.

Mitigation: Use a disposable or tightly scoped API key, avoid placing real keys in command lines or chat transcripts, and rotate any key that was already shared that way.

Risk: Company names, requested categories, API keys, and returned enterprise records are sent to and received from an external enterprise-data provider.

Mitigation: Review the external provider and data-sharing requirements before installation, and avoid submitting sensitive business queries unless the provider is approved for that use.

Risk: The skill instructs the agent to return raw API JSON without analysis or formatting, which may expose unexpected fields from provider responses.

Mitigation: Inspect returned JSON before forwarding it into downstream systems or sharing it with users who should not receive all provider-returned fields.

## Reference(s):

- [Category map](references/category-map.md)
- [ClawHub skill page](https://clawhub.ai/xinxin970620-prog/skills/rcd-enterprise)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [JSON returned from the enterprise-information API, with setup and invocation guidance in text or shell-command form]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill instructs the agent to return API JSON responses without additional analysis or formatting.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
