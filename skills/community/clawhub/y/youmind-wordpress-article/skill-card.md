## Description: <br>
Write and publish WordPress articles end-to-end with AI: topic mining via the YouMind knowledge base, de-AI voice writing, Markdown-to-HTML conversion, featured image upload, and one-click publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindy-youmind](https://clawhub.ai/user/mindy-youmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content operators use this skill to research, draft, adapt, preview, and publish WordPress posts through a YouMind-connected WordPress site. It supports draft-first publishing, media upload, taxonomy guidance, and result links for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish or change content on a connected WordPress site. <br>
Mitigation: Use draft mode by default, review generated content and metadata before publishing, and require explicit approval before using direct publish actions. <br>
Risk: The skill requires a YouMind API key connected to a WordPress account that can affect the site. <br>
Mitigation: Store the key only in the documented YouMind config location, rotate it if exposed, and connect WordPress with the least-privileged role that can perform the intended publishing tasks. <br>
Risk: The skill exposes broader site-admin actions than article drafting alone requires. <br>
Mitigation: Avoid delete, category-admin, and comment-admin commands unless those changes are explicitly requested and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindy-youmind/youmind-wordpress-article) <br>
- [YouMind WordPress OpenAPI Reference](references/api-reference.md) <br>
- [WordPress Article Pipeline](references/pipeline.md) <br>
- [WordPress Platform DNA](references/platform-dna.md) <br>
- [Generation Playbook: Idea to WordPress-Native Draft](references/content-generation-playbook.md) <br>
- [Adaptation Playbook: Existing Article to WordPress-Native](references/content-adaptation-playbook.md) <br>
- [WordPress Content Adaptation Guide](references/content-adaptation.md) <br>
- [Publishing Guidelines](shared/PUBLISHING.md) <br>
- [YouMind Home Directory](shared/YOUMIND_HOME.md) <br>
- [Dispatch Integration Protocol](shared/DISPATCH_CONTRACT.md) <br>
- [YouMind API Key Settings](https://youmind.com/settings/api-keys?utm_source=youmind-wordpress-article) <br>
- [YouMind Connector Settings](https://youmind.com/settings/connector?utm_source=youmind-wordpress-article) <br>
- [YouMind Skills Gallery](https://youmind.com/skills?utm_source=youmind-wordpress-article) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown, HTML previews, JSON API responses, configuration snippets, shell commands, and concise result summaries with links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local Markdown drafts and publish or update WordPress posts through YouMind after user setup and approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
