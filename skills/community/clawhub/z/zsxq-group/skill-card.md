## Description:

This skill guides agents in using zsxq-cli to list Knowledge Planet groups, browse group topics, inspect hashtags, and search groups or members for the logged-in account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zsxq](https://clawhub.ai/user/zsxq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to inspect Knowledge Planet groups available to a logged-in zsxq account, retrieve group, topic, and hashtag identifiers, and prepare read-only zsxq-cli commands for group browsing and member search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JSON command output can contain more account-scoped group, owner, statistics, topic, or hashtag metadata than table output.

Mitigation: Share or store JSON output only when appropriate for the logged-in zsxq account; prefer table output when full metadata is not needed.

Risk: The skill relies on an authenticated zsxq-cli session and can only access groups permitted for that account.

Mitigation: Confirm the active account and re-authenticate through the shared zsxq login guidance when a 401, token expiration, or not logged in error appears.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zsxq/skills/zsxq-group)
- [group +list reference](references/zsxq-group-list.md)
- [group +topics reference](references/zsxq-group-topics.md)
- [group +hashtags reference](references/zsxq-group-hashtags.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct use of JSON output from zsxq-cli, which can include account-scoped group, topic, owner, statistics, or hashtag metadata.]

## Skill Version(s):

1.3.1 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
