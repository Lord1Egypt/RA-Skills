## Description: <br>
Publish SEO-optimized articles to WordPress via REST API with RankMath meta fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[l1angjy](https://clawhub.ai/user/l1angjy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to let an agent create WordPress drafts or posts from structured article data, including RankMath SEO title, description, focus keyword, tags, slug, and category settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The WordPress Application Password grants REST API access to create or edit posts as the configured user. <br>
Mitigation: Use a dedicated least-privilege WordPress account, keep the .env file out of version control and shared logs, and rotate or revoke the application password when access is no longer needed. <br>
Risk: The skill can publish content publicly if publish status is selected. <br>
Mitigation: Test with draft status first, review article content before approval, and require explicit user confirmation before each publication. <br>
Risk: The WordPress PHP snippet exposes selected RankMath meta fields through the REST API. <br>
Mitigation: Keep the snippet limited to the three required meta keys, rely on edit_posts authorization, and remove the snippet if the skill is no longer in use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/l1angjy/wp-auto-post-api) <br>
- [RankMath](https://rankmath.com/) <br>
- [Code Snippets WordPress plugin](https://wordpress.org/plugins/code-snippets/) <br>
- [WordPress setup snippet](docs/wordpress-setup.php) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Console text and structured JSON result from the publishing script, with Markdown setup guidance in the skill documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates WordPress drafts by default unless the caller explicitly requests publish status and the user approves publication.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
