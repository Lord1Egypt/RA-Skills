## Description:

Weibo CLI guides agents to query Weibo public data with the `weibo` command for hot searches, searches, user profiles, feeds, post details, and comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marvae](https://clawhub.ai/user/marvae)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent retrieve and inspect public Weibo trends, posts, topics, profiles, feeds, followers, and comments through a CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned third-party npm CLI.

Mitigation: Review the package before installation, prefer a pinned local install, and avoid global installation or ad-hoc npx execution.

Risk: Providing WEIBO_COOKIE can give the CLI access to an active Weibo session.

Mitigation: Only provide the cookie when that access is acceptable, treat it like a password, and rotate or revoke it if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marvae/skills/weibo-cli)
- [Publisher profile](https://clawhub.ai/user/marvae)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands and JSON-oriented CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI examples recommend `--json` output for downstream parsing.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
