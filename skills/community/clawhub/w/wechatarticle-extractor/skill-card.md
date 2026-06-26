## Description: <br>
Extract metadata and content from WeChat Official Account articles, including titles, authors, article content, publish time, cover images, and structured fields from supported WeChat article URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xls1994](https://clawhub.ai/user/xls1994) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract WeChat Official Account article metadata and content from trusted mp.weixin.qq.com or weixin.sogou.com inputs, then save or return the result as Markdown, JSON, or HTML. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe JavaScript execution may run code derived from fetched or supplied article content. <br>
Mitigation: Use the skill only with trusted WeChat or Sogou URLs, avoid arbitrary HTML inputs, and run it in a constrained environment. <br>
Risk: Weak URL scoping may allow unexpected network scraping behavior. <br>
Mitigation: Review inputs before execution and limit use to expected mp.weixin.qq.com and weixin.sogou.com article sources. <br>
Risk: Registry-resolved npx commands and helper scripts can execute code or write to local paths. <br>
Mitigation: Prefer reviewed local commands over registry resolution, choose explicit output paths, and inspect helper scripts with hard-coded paths before running them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xls1994/wechatarticle-extractor) <br>
- [Publisher profile](https://clawhub.ai/user/xls1994) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, html, shell commands, code] <br>
**Output Format:** [Markdown files, JSON objects, HTML content, CLI console output, and JavaScript API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write extracted article output to an explicit file path or print JSON to standard output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
