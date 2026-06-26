## Description: <br>
Manage Teable resources with CRUD operations for records, bases, spaces, tables, dashboards, and trash through API-backed command-line scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[killgfat](https://clawhub.ai/user/killgfat) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers and operations users can use this skill to automate Teable workspace administration, data management, and record workflows from an agent-assisted command-line environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad data-changing and permanent deletion abilities in Teable. <br>
Mitigation: Use a least-privilege Teable token, avoid production data until tested, and require review before destructive operations. <br>
Risk: Delete, reset, and trash-emptying commands can affect the wrong resource if IDs are incorrect. <br>
Mitigation: Verify resource IDs before running destructive commands and consider adding confirmation or dry-run safeguards. <br>


## Reference(s): <br>
- [ClawHub Teable Skill](https://clawhub.ai/killgfat/teable-api) <br>
- [Teable Homepage](https://teable.io) <br>
- [Teable Official API Documentation](https://help.teable.ai/en/api-doc/overview) <br>
- [Getting IDs Guide](https://help.teable.ai/en/api-doc/get-id) <br>
- [Record Field Interface](https://help.teable.ai/en/api-doc/record/interface) <br>
- [API Error Codes](https://help.teable.ai/en/api-doc/error-code) <br>
- [Usage Examples](examples/usage_examples.md) <br>
- [Data Types and Typecast Guide](references/data-types-and-typecast.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python snippets, and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TEABLE_API_KEY and can optionally use TEABLE_URL for self-hosted Teable instances.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
