## Description:

Helps an agent organize public Zhipu AI product and documentation pages into concise summaries of model capabilities, pricing, quotas, and related links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and analysts use this skill to summarize public Zhipu AI model, pricing, quota, announcement, and documentation information. It is intended for lightweight public information organization, not account operations, API calls, or access to restricted content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may summarize stale or dynamically loaded public pricing, quota, or model capability information.

Mitigation: Review generated summaries against the cited public Zhipu AI pages before relying on them for business decisions.

Risk: Providing credentials or asking for authenticated account actions would exceed the skill's stated boundary.

Mitigation: Use the skill only for public pages and do not provide account credentials, private data, or requests for account operations.

Risk: Frequent page retrieval could conflict with platform access expectations.

Mitigation: Apply rate limits and follow the target site's published access rules when gathering public pages.

## Reference(s):

- [Zhipu AI Homepage](https://www.zhipuai.cn/)
- [ClawHub Skill Page](https://clawhub.ai/codekungfu/skills/zhipu)
- [Publisher Profile](https://clawhub.ai/user/codekungfu)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries and link lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public-page information only; no account actions, API calls, or sensitive data handling.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
