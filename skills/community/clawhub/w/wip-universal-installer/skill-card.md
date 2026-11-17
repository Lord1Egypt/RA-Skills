## Description:

Reference installer for agent-native software that scans a repository, detects which interfaces it exposes, and installs them all.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to detect agent-native interfaces in a repository and install supported CLI, module, MCP, OpenClaw plugin, skill, and Claude Code hook surfaces when the repository follows the Universal Interface conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can make persistent global and agent-configuration changes based on repository contents.

Mitigation: Review the target repository, package metadata, scripts, MCP registrations, and Claude Code hook metadata before installation; prefer an isolated environment over automatic execution on a main machine.

Risk: Remote repository targets and broad installation behavior can produce unintended CLI, MCP, OpenClaw, or hook registrations.

Mitigation: Use dry-run or JSON inspection first, then approve installation actions manually for trusted repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/parkertoddbrooks/skills/wip-universal-installer)
- [Project homepage](https://github.com/wipcomputer/wip-universal-installer)
- [Universal Interface Specification](https://github.com/wipcomputer/wip-universal-installer/blob/main/SPEC.md)
- [npm package](https://www.npmjs.com/package/@wipcomputer/universal-installer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON output from the installer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, npm, and git; installation behavior depends on the target repository interfaces.]

## Skill Version(s):

1.9.72 (source: server release metadata; artifact files also report 2.1.5 in SKILL.md metadata and CHANGELOG.md, and 1.9.68 in package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
