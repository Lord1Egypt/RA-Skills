## Description: <br>
Convert WeChat Official Account articles to clean Markdown files with locally downloaded images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soar999](https://clawhub.ai/user/soar999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to convert one or more WeChat Official Account articles into structured Markdown with article metadata and local image assets for downstream reading, archiving, or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches WeChat pages, may download a Camoufox browser, and depends on third-party Python packages. <br>
Mitigation: Install it in a virtual environment, review or pin dependencies, and run it in a network environment appropriate for fetching the target articles. <br>
Risk: The skill writes Markdown, images, and possible debug artifacts under the chosen output path. <br>
Mitigation: Use a dedicated output directory and review generated files before relying on them or sharing them. <br>
Risk: WeChat may block automated access, rate-limit requests, or show CAPTCHA verification pages. <br>
Mitigation: Use the documented non-headless/manual verification flow when needed and retry later when rate-limited. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/soar999/wechat-article-for-ai) <br>
- [Camoufox](https://github.com/nichochar/camoufox) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files] <br>
**Output Format:** [Markdown files with YAML frontmatter, local image assets, and plain text CLI or MCP status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes output under the selected output directory and can preserve remote image URLs when image download is disabled or fails.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
