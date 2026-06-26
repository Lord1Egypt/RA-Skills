## Description: <br>
Fetch and export WeChat public article content through down.mptext.top API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lniosy](https://clawhub.ai/user/lniosy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content workflows use this skill to fetch public WeChat article URLs through the down.mptext.top API and save the returned content for analysis, archiving, or downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Article URLs provided by the user are sent to the third-party down.mptext.top service. <br>
Mitigation: Use only URLs that are appropriate to share with that service, and avoid confidential, internal-only, or share-restricted links unless the service is trusted and processing is authorized. <br>
Risk: Returned article content is written to local disk. <br>
Mitigation: Choose a deliberate output directory and basename, and review generated files before sharing or using them downstream. <br>
Risk: Downloaded article content may be copyright-sensitive. <br>
Mitigation: Confirm permission to process or reuse the source material before downloading, transforming, or redistributing it. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [down.mptext.top public download API](https://down.mptext.top/api/public/v1/download) <br>
- [ClawHub release page](https://clawhub.ai/lniosy/wechat-article-download-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Local files in HTML, Markdown, text, or JSON plus command-line status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves files as the chosen basename with .html, .md, .txt, or .json extensions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
