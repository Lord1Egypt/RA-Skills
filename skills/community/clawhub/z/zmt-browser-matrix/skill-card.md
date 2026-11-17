## Description:

ZMT Matrix Browser controls a multi-account browser matrix through a local HTTP API for account listing, startup, shutdown, and information queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wociaozhongyunonghaole](https://clawhub.ai/user/wociaozhongyunonghaole)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage ZMT browser-matrix accounts over HTTP, including listing accounts and starting or stopping named browser profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control browser profiles that may contain active sessions, cookies, and account state.

Mitigation: Connect it only to browser accounts the user intends the matrix tool to control.

Risk: Unpinned Python dependencies can change behavior across installations.

Mitigation: Install in a virtual environment and prefer pinned versions of required packages.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wociaozhongyunonghaole/skills/zmt-browser-matrix)
- [ZMT Matrix Tool](https://zmt.scys6688.com/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe HTTP API control steps for browser profiles containing active sessions, cookies, and account state.]

## Skill Version(s):

1.0.16 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
