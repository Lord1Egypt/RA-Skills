## Description: <br>
Creates WeChat Official Account articles from user-provided reference materials, saves them as Markdown, and uploads them to a WeChat draft box. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CaiJichang212](https://clawhub.ai/user/CaiJichang212) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, operators, and developers maintaining WeChat Official Accounts use this skill to turn reference links, documents, or PDFs into formatted Markdown articles and upload the result to the account draft box through wenyan-cli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated articles may contain inaccurate, unsupported, or sensitive content from the supplied source material. <br>
Mitigation: Review each generated article before publishing and avoid providing confidential material unless external upload to WeChat is approved. <br>
Risk: The publishing flow requires WeChat AppID and AppSecret credentials and uploads content to a WeChat draft box. <br>
Mitigation: Keep credentials out of chat, logs, screenshots, and source control, and verify wenyan-cli configuration before running publish commands. <br>
Risk: Publishing can fail when the account IP whitelist is not configured correctly. <br>
Mitigation: Confirm the WeChat Official Account IP whitelist and local public IP before executing the upload workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/CaiJichang212/wechat-blog-write-publish) <br>
- [WeChat Official Account Developer Documentation](https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown article content with front matter, optional Mermaid diagrams, and wenyan-cli command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local Markdown, HTML, cover image, and publish-result JSON files when the publishing workflow is executed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
