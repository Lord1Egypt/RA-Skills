## Description:

Manage WordPress sites via AI Engine MCP for posts, SEO, media, taxonomies, social scheduling, multilingual content, and full admin operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site administrators, and content teams use this skill to connect an agent to AI Engine MCP and manage WordPress publishing, SEO, media, taxonomy, multilingual, ecommerce, and administrative workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can administer a live WordPress site broadly, including publishing, deleting, settings changes, plugin or theme changes, SQL, refunds, and raw REST writes.

Mitigation: Use staging or backups and require explicit confirmation before destructive or high-impact operations.

Risk: Bearer tokens can grant sensitive WordPress access if over-scoped or stored in project files.

Mitigation: Use least-privilege or separate tokens and avoid storing live tokens in shared project files.

Risk: Enabled MCP features vary by site and optional modules can expand the action surface.

Mitigation: Run tools/list before use and enable only the MCP features needed for the workflow.

## Reference(s):

- [Core WordPress Tools Reference](artifact/references/core-tools.md)
- [WordPress MCP Feature Tools Reference](artifact/references/features.md)
- [Developer Tools Reference](artifact/references/dev-tools.md)
- [SEO Engine Tools Reference](artifact/references/seo-tools.md)
- [WooCommerce Tools Reference](artifact/references/woocommerce-tools.md)
- [AI Engine WordPress plugin](https://wordpress.org/plugins/ai-engine/)
- [SEO Engine WordPress plugin](https://wordpress.org/plugins/seo-engine/)
- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/super-wordpress-mcp-0-0-0)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-RPC examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-supplied WordPress MCP URL and bearer token; available tools vary by enabled site features.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
