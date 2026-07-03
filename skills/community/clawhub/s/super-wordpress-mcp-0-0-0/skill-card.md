## Description: <br>
Manage WordPress sites via AI Engine MCP for posts, SEO, media, taxonomies, social scheduling, multilingual content, and full admin operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site operators, and content teams use this skill to guide MCP-based WordPress administration through AI Engine, including content publishing, SEO checks, media work, taxonomy updates, multilingual workflows, and optional WooCommerce or developer operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broad WordPress administration, including publishing, deleting content, changing plugins or themes, running SQL, editing WooCommerce data, changing robots.txt, and posting to social accounts. <br>
Mitigation: Require manual review and explicit user approval before executing destructive, public-facing, database, commerce, plugin, theme, robots.txt, or social-posting actions. <br>
Risk: Connection setup stores powerful bearer tokens in project notes such as TOOLS.md. <br>
Mitigation: Use least-privilege tokens where possible, never commit real tokens, rotate exposed tokens immediately, and keep credentials out of shared repositories. <br>
Risk: Available MCP tools vary by site configuration, so assumptions about enabled capabilities can lead to failed or unintended operations. <br>
Mitigation: Start each site session with tools/list and limit actions to tools confirmed as enabled for that site. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/subaru0573/skills/super-wordpress-mcp-0-0-0) <br>
- [AI Engine WordPress Plugin](https://wordpress.org/plugins/ai-engine/) <br>
- [SEO Engine WordPress Plugin](https://wordpress.org/plugins/seo-engine/) <br>
- [Core WordPress Tools Reference](references/core-tools.md) <br>
- [Developer Tools Reference](references/dev-tools.md) <br>
- [WordPress MCP Feature Tools Reference](references/features.md) <br>
- [SEO Engine Tools Reference](references/seo-tools.md) <br>
- [WooCommerce Tools Reference](references/woocommerce-tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON-RPC examples and bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance depends on the WordPress MCP features enabled by the site administrator.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
