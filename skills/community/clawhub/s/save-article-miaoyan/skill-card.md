## Description:

Saves web articles to Miaoyan by fetching readable content, generating a short summary, and writing a Markdown note to the Miaoyan 待学习 folder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vlalamoon](https://clawhub.ai/user/vlalamoon)

### License/Terms of Use:

MIT-0

## Use Case:

External users who save WeChat and other web articles into Miaoyan use this skill to fetch readable content, summarize it, and create local Markdown notes in an iCloud-synced Miaoyan folder.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article URLs may be sent to external extraction providers.

Mitigation: Do not use the skill with private, tokenized, internal, signed, or sensitive URLs unless confirmation and URL allowlisting are added.

Risk: WeChat article links can be saved automatically without a user confirmation step.

Mitigation: Review the trigger configuration and require explicit confirmation before automatic saves in shared or sensitive environments.

Risk: Fetched article content is written to a fixed iCloud-synced Miaoyan folder.

Mitigation: Confirm the storage policy for synced notes and change the target folder before deployment when local-only storage is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vlalamoon/skills/save-article-miaoyan)
- [Tavily](https://tavily.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown notes plus plain-text or JSON status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes fetched article content and generated summaries to a fixed Miaoyan/iCloud folder; may call external extraction providers.]

## Skill Version(s):

2.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
