## Description:

Manage YouTube memberships levels. Use this skill to list information about channel membership levels. Useful when working with YouTube memberships level - provides commands to list memberships level via the yutu CLI. Includes setup and installation instructions for first-time users. Triggers: list memberships levels, list memberships level, list my memberships level

This skill is ready for commercial/non-commercial use.

## Publisher:

[openwaygate](https://clawhub.ai/user/openwaygate)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect YouTube channel membership level information through the yutu CLI after configuring YouTube API OAuth credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned third-party yutu CLI.

Mitigation: Install a pinned and verified yutu release where possible, and review the tool before use.

Risk: YouTube OAuth client secrets and cached tokens are stored locally.

Mitigation: Keep client_secret.json and youtube.token.json outside source-controlled folders, restrict file permissions, and revoke or rotate the OAuth token if either file is exposed.

Risk: The skill can access YouTube API data once OAuth credentials are configured.

Mitigation: Use a non-privileged account and grant only the access needed for the intended channel membership-level lookup.

## Reference(s):

- [Memberships Level List](references/membershipsLevel-list.md)
- [Yutu Setup Guide](references/setup.md)
- [yutu project homepage](https://github.com/eat-pray-ai/yutu)
- [yutu README](https://github.com/eat-pray-ai/yutu#readme)
- [yutu releases](https://github.com/eat-pray-ai/yutu/releases/latest)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports table, JSON, and YAML output from the yutu CLI when the agent runs the documented command.]

## Skill Version(s):

0.10.7-dev (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
