## Description:

spool helps agents use the OpenClaw browser tool to read, post, reply, view profiles, and search on Meta Threads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zizi-cat](https://clawhub.ai/user/zizi-cat)

### License/Terms of Use:


## Use Case:

Developers and agents use spool to operate a logged-in Threads account through OpenClaw browser automation for timeline reading, publishing posts, replying, viewing profiles, and search. Publishing workflows should include user confirmation before content is posted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented optional headless setup installs a persistent system-wide Xvfb service with administrator privileges and no cleanup path.

Mitigation: Review before installing on shared or production machines, prefer a temporary or user-scoped Xvfb setup, and document how to disable or remove the service.

Risk: The skill can post or reply from a logged-in Threads account.

Mitigation: Require explicit confirmation of the exact Threads post or reply target and content before publishing.

Risk: Browser element references can change between snapshots, which can cause actions to target the wrong element.

Mitigation: Take a fresh snapshot immediately before each browser action and verify the referenced element before clicking or typing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zizi-cat/skills/spool)
- [spool homepage](https://github.com/zizi-cat/spool)
- [Threads](https://www.threads.net)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, browser tool commands]

**Output Format:** [Markdown with browser tool commands and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an OpenClaw browser profile logged in to Threads; browser element refs must be refreshed from snapshots before actions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
