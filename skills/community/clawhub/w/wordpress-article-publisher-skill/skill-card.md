## Description: <br>
Generates structured articles from user-provided keywords and publishes them to a WordPress site through the WordPress REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuxucai](https://clawhub.ai/user/liuxucai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and site operators use this skill to draft keyword-based WordPress articles, configure publishing parameters, and run PowerShell scripts that create, update, or delete posts through the WordPress REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use WordPress credentials to publish content to a live site. <br>
Mitigation: Use a least-privilege WordPress application password, verify the target domain before publishing, and prefer draft status until content is reviewed. <br>
Risk: The skill includes deletion and delete-and-repost workflows that can remove live content. <br>
Mitigation: Confirm the post ID and keep a backup before deletion, and prefer in-place updates when possible. <br>
Risk: Incorrect credentials, API URLs, or post IDs can cause failed operations or unintended changes. <br>
Mitigation: Validate the WordPress REST API endpoint, username, application password, and post ID before running the PowerShell scripts. <br>


## Reference(s): <br>
- [WordPress REST API Reference](references/api-reference.md) <br>
- [WordPress Application Password Setup](references/wordpress-setup.md) <br>
- [Chinese Encoding Fix](references/encoding-fix.md) <br>
- [ClawHub Release Page](https://clawhub.ai/liuxucai/wordpress-article-publisher-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with PowerShell command examples and WordPress post content in HTML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate article drafts, WordPress publishing commands, post status settings, category or tag parameters, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
