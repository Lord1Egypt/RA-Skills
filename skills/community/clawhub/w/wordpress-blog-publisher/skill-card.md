## Description: <br>
Use this skill whenever the user wants to publish, update, or batch-upload blog content to a WordPress site via the REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leooooooow](https://clawhub.ai/user/leooooooow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, developers, and publishing teams use this skill to publish, update, schedule, and batch-upload WordPress posts through the WordPress REST API while preserving content formatting, media handling, taxonomy IDs, and upstream status tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use WordPress application-password credentials and change live WordPress content. <br>
Mitigation: Use a dedicated least-privilege WordPress user, store credentials in environment variables or a secret manager, and explicitly confirm live publish, update, batch, or remote media operations. <br>
Risk: Batch publishing can propagate formatting, taxonomy, media, or scheduling mistakes across many posts. <br>
Mitigation: Run and review a dry-run or first-post validation before processing the remaining batch, keep error logging enabled, and review the final publish summary. <br>
Risk: Credential or site configuration files may expose sensitive access if committed. <br>
Mitigation: Do not commit config/sites.json or secrets; keep site credentials outside source control. <br>


## Reference(s): <br>
- [WordPress REST API Quick Reference](artifact/references/api-reference.md) <br>
- [Markdown to HTML Conversion Rules](artifact/references/markdown-to-html-rules.md) <br>
- [WordPress Publishing Quality Checklist](artifact/assets/wp-publish-checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/leooooooow/wordpress-blog-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, JSON examples, REST API calls, checklists, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run and confirmation steps before live publish, update, batch, or remote media operations.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
