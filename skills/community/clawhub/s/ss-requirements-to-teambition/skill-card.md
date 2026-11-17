## Description:

Collects tagged SaleSmartly support conversations, analyzes them for customer requirements or bugs, and creates Teambition tasks for feedback-to-requirements automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zpeng6834-arch](https://clawhub.ai/user/zpeng6834-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Support and product operations teams use this skill to turn tagged SaleSmartly conversations into structured Teambition requirements or bug tasks. It supports incremental collection, AI-assisted conversation analysis, duplicate checks, and task creation or note updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A likely real SaleSmartly API key is bundled in the artifact configuration.

Mitigation: Revoke and remove the bundled key before installation, then provide SaleSmartly credentials through a protected secret mechanism.

Risk: Customer conversation content may be copied into local JSON files and Teambition tasks.

Mitigation: Restrict access to the generated data directory and Teambition project, and add human review or redaction before customer conversations are copied into tasks.

Risk: The workflow depends on a Teambition MCP package and user token with task-write permissions.

Mitigation: Pin and review the MCP package, store Teambition tokens outside the artifact, and limit token permissions and access where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zpeng6834-arch/skills/ss-requirements-to-teambition)
- [AI Analysis and Task Creation Template](references/analysis_template.md)
- [Configuration Fields Guide](references/config_fields.md)
- [Execution Guide](references/execution_guide.md)
- [Teambition MCP Setup Guide](references/tb_mcp_setup.md)
- [Teambition User MCP](https://open.teambition.com/user-mcp)
- [SaleSmartly API Endpoint](https://api.salesmartly.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance, JSON configuration, shell commands, SaleSmartly session JSON files, and Teambition task or note update requests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The collection script writes dated session JSON files under scripts/data and keeps them for seven days; task creation depends on SaleSmartly API access and a configured Teambition MCP server.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
