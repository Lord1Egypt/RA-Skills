## Description:

Hook that blocks destructive edits to protected identity files. For Claude Code CLI and OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install and configure a file-edit guard that blocks overwrites or destructive edits to protected identity, memory, and shared-context files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks this release as suspicious because broad path exceptions and fail-open behavior need review before installation.

Mitigation: Review and scan the skill before deployment; address path canonicalization, malformed protected-file events, and test/documentation alignment with the intended policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/parkertoddbrooks/skills/wip-file-guard)
- [Publisher profile](https://clawhub.ai/user/parkertoddbrooks)
- [Project homepage](https://github.com/wipcomputer/wip-file-guard)
- [npm package](https://www.npmjs.com/package/@wipcomputer/wip-file-guard)
- [Manual install and reference](REFERENCE.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with shell and JSON configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce hook configuration and command-line usage guidance for Claude Code, OpenClaw, and direct CLI use.]

## Skill Version(s):

1.9.72 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
