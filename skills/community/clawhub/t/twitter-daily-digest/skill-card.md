## Description:

Fetches recent Twitter/X posts from followed or specified accounts, saves objective tweet data as JSON, and guides the agent to create a Chinese daily digest that can be shared locally, in chat, and in Notion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ceylonlatte](https://clawhub.ai/user/ceylonlatte)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal productivity agents use this skill to gather recent Twitter/X activity from authenticated account access, then turn the resulting facts into a readable Chinese daily digest. It supports full following-list digests, sampled runs, named-account checks, local Markdown output, chat delivery, and optional Notion sync.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses authenticated Twitter/X account access to read following activity.

Mitigation: Install it only for workflows where this access is intended, and pin and verify the twitter-cli dependency before use.

Risk: Digest content can be persisted locally under the user's home/Desktop area.

Mitigation: Review the configured output path and generated Markdown before treating the digest as final.

Risk: The skill can publish the finished digest into the configured Notion parent page.

Mitigation: Check the Notion parent page, scope the Notion API key appropriately, and require explicit confirmation before running Notion sync.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ceylonlatte/skills/twitter-daily-digest)
- [Publisher profile](https://clawhub.ai/user/ceylonlatte)
- [Notion parent page configured by the skill](https://www.notion.so/323dfb80f233811ab597f30cb2013145)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON facts, Markdown digest content, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script produces objective Twitter/X facts; the agent performs subjective selection, grouping, translation, and final Chinese digest writing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
