## Description: <br>
Publish content directly to WordPress sites via REST API with full Gutenberg block support, category selection, SEO tag generation, preview workflows, and markdown or HTML conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Asif2BD](https://clawhub.ai/user/Asif2BD) <br>

### License/Terms of Use: <br>
GPL v3 <br>


## Use Case: <br>
Developers, editors, and publishing teams use this skill to convert markdown or HTML into Gutenberg blocks and create, preview, schedule, or publish WordPress posts and pages through the WordPress REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform live WordPress write operations, including publishing, updating, deleting content, and creating categories or tags. <br>
Mitigation: Install only for WordPress sites you control, default to draft and preview workflows, and require explicit confirmation before publishing, updating, deleting, or creating taxonomy entries. <br>
Risk: The skill handles WordPress application passwords and authenticated REST API access. <br>
Mitigation: Use a least-privilege WordPress application password, avoid passing credentials directly in shell commands, and verify the site URL before connecting. <br>
Risk: Generated Gutenberg content may render differently from the source markdown or HTML after conversion. <br>
Mitigation: Preview draft posts, validate Gutenberg block structure, and verify the rendered page before making content public. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/Asif2BD/wordpress-publishing-skill-for-claude) <br>
- [Publisher profile](https://clawhub.ai/user/Asif2BD) <br>
- [Gutenberg blocks reference](references/gutenberg-blocks.md) <br>
- [WordPress REST API Handbook](https://developer.wordpress.org/rest-api/) <br>
- [WordPress Core Blocks Reference](https://developer.wordpress.org/block-editor/reference-guides/core-blocks/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance, Python examples, shell commands, and Gutenberg-compatible HTML blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify WordPress posts, pages, categories, tags, and media when used with live credentials.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
