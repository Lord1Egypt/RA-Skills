## Description: <br>
Exports WeChat public-account articles from mp.weixin.qq.com URLs as long screenshots while preserving the article layout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benzking](https://clawhub.ai/user/benzking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content archivists use this skill to capture permitted WeChat public-account articles as PNG screenshots and PDF exports from mp.weixin.qq.com URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Playwright browser automation that disguises automation and disables some browser protections. <br>
Mitigation: Run it in an isolated workspace with a fresh browser profile and review the browser behavior before use. <br>
Risk: Automated capture of WeChat articles may conflict with site, account, or content-owner rules if used without authorization. <br>
Mitigation: Use it only for articles you are allowed to archive and confirm compliance with applicable site, account, and content rules. <br>
Risk: Generated screenshots and PDFs can contain sensitive article content. <br>
Mitigation: Store outputs in approved locations and review files before sharing them. <br>


## Reference(s): <br>
- [WeChat Article Exporter on ClawHub](https://clawhub.ai/benzking/wechat-article-exporter) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, files, guidance] <br>
**Output Format:** [Markdown instructions with shell command execution and generated PNG/PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a valid https://mp.weixin.qq.com/s/ article URL and an output directory.] <br>

## Skill Version(s): <br>
3.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
