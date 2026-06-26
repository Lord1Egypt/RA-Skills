## Description: <br>
Converts public WeChat Official Account article pages into clean Markdown for extraction, saving, or archiving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benzking](https://clawhub.ai/user/benzking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and content archivists use this skill to convert public WeChat articles into Markdown files with article metadata and optional local image assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches WeChat article pages and image CDN URLs over the network. <br>
Mitigation: Run it only on public WeChat URLs you trust, expect outbound requests to WeChat and image hosts, and use --no-images when local media retention is not needed. <br>
Risk: Converted Markdown and downloaded images are saved under the selected output directory. <br>
Mitigation: Use an isolated output folder when converting articles that should not leave retained files in a sensitive workspace. <br>
Risk: Login-gated articles, captcha pages, restricted pages, or code rendered as images may produce incomplete or failed conversions. <br>
Mitigation: Review the generated Markdown against the source article before relying on it, and preserve the source URL in frontmatter for traceability. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/benzking/wechat-article-to-markdown-v2) <br>
- [WeChat DOM Reference](references/wechat-dom-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files with optional YAML frontmatter, local image assets, and programmatic metadata dictionaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can download article images into an images subdirectory unless --no-images is used; preserves remote image URLs when downloads fail or are disabled.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata, created 2026-04-11T05:14:16Z) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
