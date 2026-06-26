## Description: <br>
A text-auditing skill that combines local rule scanning, Baidu content review APIs, and AI analysis to prepare compliance-review prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahsbnb](https://clawhub.ai/user/ahsbnb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content reviewers and agents use this skill to audit Chinese text for marketing and platform-compliance risks, then generate a prompt for a detailed audit report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reviewed text or images may be sent to Baidu cloud services. <br>
Mitigation: Use the skill only with content you are permitted to send to Baidu, and avoid confidential, regulated, or personal content unless the data handling is approved. <br>
Risk: The skill stores and uses Baidu API credentials from local configuration. <br>
Mitigation: Protect the local configuration file, use appropriately scoped credentials, and rotate keys if they may have been exposed. <br>
Risk: Compliance rewrites and safe verdicts can still be incomplete or wrong. <br>
Mitigation: Treat generated safe versions as lower-risk drafts and require human review before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ahsbnb/robust-text-auditor) <br>
- [WeChat Channels content guidance referenced by the audit prompt](https://weixin.qq.com/cgi-bin/readtemplate?lang=zh_CN&t=weixin_agreement&s=video_guide) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Generated prompt text with local scan and Baidu API results for downstream report generation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires one input text string or text file; Baidu API credentials must be configured locally.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
