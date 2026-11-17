## Description:

Command-line tool for searching, reading, and interacting with Zhihu (知乎). Supports hot topics, content search, article reading, user info, and Browser Relay-based voting/following.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lightislost](https://clawhub.ai/user/lightislost)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to install and operate the zhihu-cli command-line tool for searching, reading, and interacting with Zhihu content. It also supports login-dependent workflows such as voting and following through cookie setup and Browser Relay instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned external npm CLI that can access a Chrome Zhihu session.

Mitigation: Install only after reviewing or pinning the package version and confirming the package's credential handling behavior.

Risk: The CLI stores Zhihu cookies locally and may expose manually entered cookie strings through logs or shell history.

Mitigation: Treat ~/.zhihu-cookie and entered cookie strings like passwords, avoid sharing logs or shell history containing them, and remove stored cookies when no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lightislost/skills/zhihu-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that install or invoke an external npm package and guidance for handling Zhihu cookies.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
