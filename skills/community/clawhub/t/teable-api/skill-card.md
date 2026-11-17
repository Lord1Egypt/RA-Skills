## Description:

Manage Teable resources with CRUD operations for records, bases, spaces, tables, dashboards, and trash through API-backed command-line scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[killgfat](https://clawhub.ai/user/killgfat)

### License/Terms of Use:

MIT License

## Use Case:

Developers and operators use this skill to manage Teable workspaces and data from an agent workflow, including administrative actions such as collaborator, dashboard, table, record, and trash operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform broad live data-changing Teable actions, including delete, trash reset, collaborator, invitation, and plugin commands.

Mitigation: Review proposed commands before execution and use a least-privilege Teable token scoped to the intended workspace and operation.

Risk: The skill relies on TEABLE_API_KEY and can target custom Teable endpoints through TEABLE_URL.

Mitigation: Avoid storing tokens in shell startup files, rotate exposed tokens, and use only trusted HTTPS Teable URLs.

## Reference(s):

- [Teable Official Documentation](https://help.teable.ai/en/api-doc/overview)
- [Getting IDs Guide](https://help.teable.ai/en/api-doc/get-id)
- [Record Field Interface](https://help.teable.ai/en/api-doc/record/interface)
- [API Error Codes](https://help.teable.ai/en/api-doc/error-code)
- [Data Types and Typecast Guide](references/data-types-and-typecast.md)
- [Teable Skill Page](https://clawhub.ai/killgfat/skills/teable-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include commands that call live Teable APIs using TEABLE_API_KEY and optional TEABLE_URL.]

## Skill Version(s):

1.0.6 (source: ClawHub release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
