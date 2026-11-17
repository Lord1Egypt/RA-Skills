## Description:

Reads profiles, posts, search results, and signed-in account activity on X, and previews user-requested posts before publishing them through the X API v2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odrobnik](https://clawhub.ai/user/odrobnik)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents use this skill to look up X profiles and posts, search recent posts, read their signed-in account's home timeline, bookmarks, and likes, or draft and publish an approved post.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access to X developer credentials and private signed-in account data.

Mitigation: Keep configuration and sign-in tokens private; share private account data only as requested, and log out or revoke the connected app when finished.

Risk: Publishing unintended content to the signed-in X account.

Mitigation: Review the exact post preview and obtain explicit approval before publishing.

Risk: X API requests may incur charges.

Mitigation: Set X API spending limits and keep requests limited to what is needed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/odrobnik/skills/x-api-v2)
- [Publisher-listed skill homepage](https://github.com/odrobnik/x-skill)
- [Setup guide](SETUP.md)
- [X API pricing guide](references/pricing.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Text or JSON responses and Markdown instructions with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Post preview requires explicit approval before publication; X API usage may incur charges.]

## Skill Version(s):

1.2.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
