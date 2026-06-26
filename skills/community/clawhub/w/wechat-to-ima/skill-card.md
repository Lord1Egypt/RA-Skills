## Description: <br>
Save WeChat Official Account articles into IMA notes or a named IMA knowledge base while preserving article structure and images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harven-droid](https://clawhub.ai/user/harven-droid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to import trusted WeChat Official Account articles into IMA notes or a selected IMA knowledge base without manual copying. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires IMA API credentials and can access user note or knowledge-base destinations. <br>
Mitigation: Use narrowly scoped IMA credentials where possible and run the skill only in a trusted local environment. <br>
Risk: The security review notes that fetched page content is parsed while IMA credentials are available. <br>
Mitigation: Use the skill only for trusted WeChat or Sogou links until host validation and parsing hardening are implemented. <br>
Risk: The security guidance notes that a Markdown copy may remain in a temporary directory. <br>
Mitigation: Review and delete temporary Markdown files after importing sensitive articles. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harven-droid/wechat-to-ima) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [JSON status output and Markdown article content submitted to IMA] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IMA credentials; may write a temporary Markdown copy during import.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
