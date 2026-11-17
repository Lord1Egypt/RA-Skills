## Description:

Provides full read and write access to Skool communities through an Apify actor for posts, comments, members, events, mentions, and community management tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ctala](https://clawhub.ai/user/ctala)

### License/Terms of Use:

MIT-0

## Use Case:

External community operators and developers use this skill to manage Skool communities through Apify. It supports reading and creating posts, replying to comments, managing pending members, banning members, listing events, and preparing user mentions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to send Skool passwords, reusable session cookies, private community data, and Apify account access to a third-party Apify actor.

Mitigation: Use a dedicated low-privilege Skool automation account, a least-privilege Apify token, and approved credential handling before running the actor.

Risk: The skill can perform high-impact community actions such as posting, editing, deleting, approving, rejecting, and banning members.

Mitigation: Require manual confirmation and review the exact action, target IDs, and payload before any destructive, administrative, or public write action.

Risk: Reusable Skool cookies can remain valid for several days after login.

Mitigation: Store cookies securely, avoid exposing them in logs or chat transcripts, and revoke or refresh sessions when automation is complete or authentication errors occur.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ctala/skills/skool-all-in-one-api)
- [Apify Actor Page](https://apify.com/cristiantala/skool-all-in-one-api)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API calls, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request payloads, action checklists, and human-readable summaries of Skool posts, comments, members, or events.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
