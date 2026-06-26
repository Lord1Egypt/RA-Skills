## Description: <br>
Manage WordPress sites via MCP through AI Engine for content editing, SEO analysis, analytics, media, taxonomies, social scheduling, multilingual workflows, ecommerce, and related WordPress administration tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jordymeow](https://clawhub.ai/user/jordymeow) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, site operators, and content teams use this skill to administer WordPress sites through an AI Engine MCP endpoint, including content publishing, media, taxonomies, SEO workflows, multilingual content, ecommerce, and optional developer operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad live-site authority could allow unintended changes to content, users, settings, code, database records, ecommerce data, or public publishing. <br>
Mitigation: Use the least-privileged bearer token available, keep optional MCP features disabled unless needed, and require explicit human approval before public, destructive, financial, user-management, settings, database, or code-changing actions. <br>
Risk: SQL, Dynamic REST, plugin editing, and theme editing can create production outages or security exposure. <br>
Mitigation: Avoid enabling or using these capabilities on production sites unless there is a reviewed operational need and a rollback path. <br>
Risk: Bearer tokens stored in local configuration can grant direct access to the WordPress MCP endpoint if exposed. <br>
Mitigation: Do not commit tokens, scope them to a specific site and role where possible, and rotate them if they may have been shared. <br>


## Reference(s): <br>
- [ClawHub WordPress MCP release page](https://clawhub.ai/jordymeow/wordpress-mcp) <br>
- [AI Engine WordPress plugin](https://wordpress.org/plugins/ai-engine/) <br>
- [SEO Engine WordPress plugin](https://wordpress.org/plugins/seo-engine/) <br>
- [Core WordPress Tools Reference](references/core-tools.md) <br>
- [Feature Tools Reference](references/features.md) <br>
- [Developer Tools Reference](references/dev-tools.md) <br>
- [WooCommerce Tools Reference](references/woocommerce-tools.md) <br>
- [SEO Engine Tools Reference](references/seo-tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON-RPC examples, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are agent instructions and proposed MCP calls; site-side effects depend on the enabled AI Engine MCP tools and token permissions.] <br>

## Skill Version(s): <br>
3.3.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
