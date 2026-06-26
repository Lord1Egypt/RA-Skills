## Description: <br>
Auto-generates SEO-optimized HTML articles using DeepSeek AI to help drive organic traffic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duoduoks](https://clawhub.ai/user/duoduoks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Website operators and content teams use this skill to generate Chinese SEO articles on configured topics, write HTML article files, and keep a sitemap updated for search indexing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive API credentials and may read local OpenClaw or DeepSeek credential configuration. <br>
Mitigation: Install only in trusted website workspaces, prefer explicit environment-based credentials, and verify credential access before execution. <br>
Risk: The skill performs recurring website file changes by creating article pages and modifying sitemap.xml. <br>
Mitigation: Review the configured output directory and scheduling behavior, keep changes under version control, and require manual approval where automatic publication is not desired. <br>
Risk: Generated SEO content may contain inaccurate, low-quality, or unsuitable claims for a published site. <br>
Mitigation: Review generated articles before publishing and apply editorial, legal, and brand checks for the target website. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/duoduoks/seo-article-generator) <br>
- [Publisher profile](https://clawhub.ai/user/duoduoks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and generated HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes article HTML under an articles directory and updates sitemap.xml when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
