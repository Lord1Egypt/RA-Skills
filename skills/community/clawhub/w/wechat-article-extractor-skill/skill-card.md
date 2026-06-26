## Description: <br>
Extracts metadata, content, account details, and media fields from WeChat Official Account article URLs or saved HTML. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freestylefly](https://clawhub.ai/user/freestylefly) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to extract structured article metadata and content from WeChat Official Account URLs or saved HTML, including account information, publish time, cover image, and article body fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Parsing pages carries a code-execution risk according to the ClawHub security evidence. <br>
Mitigation: Review before installing, run only in a sandbox or low-privilege environment, avoid arbitrary links or pasted HTML, and prefer a version that parses metadata without new Function/eval. <br>
Risk: The bundled .claude/settings.local.json broadens tool access. <br>
Mitigation: Remove .claude/settings.local.json unless those MCP server settings are intentionally required. <br>
Risk: Untrusted article URLs or page content may lead to unsafe fetch or parsing behavior. <br>
Mitigation: Validate the actual URL hostname, avoid following untrusted transfer links, and restrict network access when processing articles. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freestylefly/wechat-article-extractor-skill) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples and JSON-shaped extraction results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns success or error objects; successful results may include article metadata, account fields, HTML content, cover image URLs, source links, and publish timestamps.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
