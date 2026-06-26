## Description: <br>
WordPress.com API integration with managed OAuth for managing posts, pages, sites, and site content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to interact with WordPress.com through Maton-managed OAuth, including listing, creating, updating, and deleting posts and pages and managing site and account content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Maton API keys and WordPress.com OAuth connections can authorize broad account and content access. <br>
Mitigation: Install only if you trust Maton to mediate OAuth access, keep MATON_API_KEY private, and review the connected WordPress.com account before use. <br>
Risk: Write-capable endpoints can publish, edit, delete, like or unlike content, list site users, or change account settings. <br>
Mitigation: Require explicit user confirmation before any write operation or sensitive account action, including the target resource and intended effect. <br>
Risk: When multiple WordPress.com connections exist, requests may affect the wrong account or site. <br>
Mitigation: Use the Maton-Connection header for multi-account setups and confirm the target connection, site, and resource before executing requests. <br>


## Reference(s): <br>
- [ClawHub WordPress Skill](https://clawhub.ai/byungkyu/wordpress-api) <br>
- [WordPress.com REST API Overview](https://developer.wordpress.com/docs/api/) <br>
- [WordPress.com REST API Getting Started](https://developer.wordpress.com/docs/api/getting-started/) <br>
- [WordPress.com REST API Reference](https://developer.wordpress.com/docs/api/rest-api-reference/) <br>
- [WordPress.com OAuth Authentication](https://developer.wordpress.com/docs/oauth2/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with API endpoint descriptions and Python, JavaScript, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a valid WordPress.com OAuth connection mediated by Maton.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
