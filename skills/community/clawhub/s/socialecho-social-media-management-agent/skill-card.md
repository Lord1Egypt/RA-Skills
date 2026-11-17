## Description:

Use SocialEcho OpenAPI for explicit team/account/content queries and user-authorized TikTok Shop sync or cross-platform publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socialecho-net](https://clawhub.ai/user/socialecho-net)

### License/Terms of Use:

MIT-0

## Use Case:

External operators and developers use this skill to manage SocialEcho-backed social media workflows with an explicitly supplied Team API Key. It supports team, account, content, report, upload, Reddit, Pinterest, TikTok Shop product, and TikTok music queries, plus user-authorized TikTok Shop sync and cross-platform publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A powerful SocialEcho Team API Key can leak through shell history, process listings, or shared logs when passed on the command line.

Mitigation: Use a narrowly scoped and easily revocable key, avoid pasting real keys into shared command examples or logs, and rotate any key that may have been exposed.

Risk: Publishing articles or syncing TikTok Shop products can make live changes to connected social accounts or shop data.

Mitigation: Review the dry-run preview, confirm the exact target account and payload, and run live writes only after current explicit authorization with a matching confirmation account ID.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/socialecho-net/skills/socialecho-social-media-management-agent)
- [SocialEcho Social Media OpenAPI](artifact/openapi.json)
- [Platform publish limits: copy, media, and formats](artifact/platform-publish-limits_en.md)
- [Platform publish limits, Chinese](artifact/platform-publish-limits_cn.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses or dry-run previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=18 and an explicitly supplied SocialEcho Team API Key; live writes require dry-run review, --execute, and a matching --confirm-account-id.]

## Skill Version(s):

2.1.1 (source: server release evidence, package.json, _meta.json, and openapi.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
