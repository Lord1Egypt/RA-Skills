## Description:

Builds, updates, runs, and validates a local SmartLink / Zhijietong cross-border ecommerce intellectual-property HTML workbench with Patsnap-supported patent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and solution engineers use this skill to maintain a local HTML product workbench for infringement complaints, listing compliance, competitor patent analysis, and IP knowledge support. It guides file edits, local preview, Patsnap MCP setup, and validation for customer-facing demonstrations or operational workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run unreviewed local Patsnap proxy code from a hard-coded machine path.

Mitigation: Install only in trusted local environments and verify or bundle the proxy script before running proxy commands.

Risk: The skill serves a broad local Downloads directory for preview.

Mitigation: Restrict the preview server to a dedicated project folder before use.

Risk: The skill writes backup and latest-copy files to hard-coded local paths.

Mitigation: Make destination paths configurable and require confirmation before overwriting or copying files.

Risk: Security evidence marks the release as suspicious because of local execution, broad serving scope, and hard-coded backup behavior.

Mitigation: Review the skill and scanner guidance before deployment, and limit execution to a sandboxed or otherwise controlled workstation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/smartlink-ip-workbench)
- [Competitor Analysis Implementation Notes](references/competitor-analysis.md)
- [Patsnap Open Platform](https://open.zhihuiya.com/)
- [Patsnap MCP server marketplace](https://open.zhihuiya.com/marketplace/mcp-servers)
- [Patsnap API key authentication guide](https://open.zhihuiya.com/devportal/guides/authentication)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code edits, shell commands, file links, and validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local HTML files, timestamped backup copies, and latest-version copies when used in its intended local workspace.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
