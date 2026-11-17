## Description:

Convert timezones, resolve natural language times, compute durations, and adjust timestamps with DST awareness after a one-time local MCP server install.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billylui](https://clawhub.ai/user/billylui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to normalize ambiguous time expressions, convert dates across IANA timezones, compute durations, and make DST-aware timestamp adjustments before scheduling or time-sensitive work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs a third-party MCP binary during setup.

Mitigation: Use the pinned package path, verify published checksums before first use, and avoid elevated privileges.

Risk: Initial installation may contact external package and release hosts.

Mitigation: Use the documented Docker containment with network isolation after setup when stronger isolation is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/billylui/skills/temporal-cortex-datetime)
- [Temporal Cortex homepage](https://temporal-cortex.com)
- [Repository listed in metadata](https://github.com/temporal-cortex/skills)
- [npm package](https://www.npmjs.com/package/@temporal-cortex/cortex-mcp)
- [Release checksums](https://github.com/temporal-cortex/mcp/releases/download/mcp-v0.9.1/SHA256SUMS.txt)
- [Datetime Tools Reference](references/DATETIME-TOOLS.md)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Structured text and RFC 3339 timestamp values returned through MCP tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only datetime computations; no credentials are required.]

## Skill Version(s):

0.9.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
