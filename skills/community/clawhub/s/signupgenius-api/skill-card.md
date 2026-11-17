## Description:

Access SignUpGenius (sign-ups, groups, RSVPs) from a shell with curl instead of running the signupgenius-mcp server — server-side email/password login to a JWT + cfid/cftoken cookies, then curl the v3 API and legacy /SUGboxAPI.cfm dispatcher directly. Use when you want SignUpGenius data without the MCP, in a script, or on a machine where the MCP isn't installed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use curl and jq to inspect SignUpGenius profiles, groups, sign-ups, and public slot details, or to submit RSVP and slot actions from scripts without running signupgenius-mcp.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Login and personal data may be exposed through inadequately protected temporary files; live service permissions and slot-write recipes were not tested.

Mitigation: Use a private temporary directory with restrictive permissions and automatic cleanup for cookies, headers, and signup data. Keep passwords and tokens out of logs and shell history, limit personal-data access to authorized tasks, and retain confirmation and ownership checks before writes.

## Reference(s):

- [SignUpGenius session-mode endpoints](artifact/references/sug-endpoints.md)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with curl commands, jq filters, and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

2.2.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
