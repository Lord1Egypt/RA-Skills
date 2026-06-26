## Description: <br>
Publishes Markdown articles to a Typecho blog over XML-RPC, with file-based publishing, draft mode, tag handling, and image selection or upload workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiliangseason-arch](https://clawhub.ai/user/jiliangseason-arch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Blog operators, developers, and content publishers use this skill to prepare, preview, and publish Markdown posts to Typecho blogs through XML-RPC. It supports drafting, tag and category metadata, image handling, and operational scripts for managing published content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate with admin-level control over a Typecho blog. <br>
Mitigation: Use a least-privileged or test account where possible, keep BLOG_PASSWORD out of source control, and limit access to the configured environment file. <br>
Risk: Publishing, bulk modification, cleanup, and deletion paths can change public blog content immediately. <br>
Mitigation: Prefer draft workflows, preview posts before public release, keep backups, and review cleanup or delete commands before running them. <br>
Risk: Remote image URL workflows can download and upload third-party media into the blog. <br>
Mitigation: Review image source, license, and URL before allowing the skill to download or upload the asset. <br>
Risk: Generated or transformed article metadata may produce incorrect titles, categories, tags, or image rendering. <br>
Mitigation: Open the resulting post or draft and verify title, category, tags, formatting, and image display before considering publication complete. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jiliangseason-arch/typecho-blog-publish) <br>
- [Article Template](artifact/references/article-template.md) <br>
- [Usage Examples](artifact/references/examples.md) <br>
- [Markdown Guide](artifact/references/markdown-guide.md) <br>
- [Troubleshooting](artifact/references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; generated blog posts are Markdown content published through XML-RPC workflows.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Typecho blog credentials through BLOG_PASSWORD, with optional BLOG_URL, BLOG_USERNAME, and BLOG_XMLRPC configuration.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
