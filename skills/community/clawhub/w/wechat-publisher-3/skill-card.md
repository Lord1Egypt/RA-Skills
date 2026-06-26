## Description: <br>
Automates WeChat public-account content workflows by collecting hot topics, generating articles, formatting them as WeChat-ready HTML, and publishing drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyy1976](https://clawhub.ai/user/andyy1976) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and WeChat public-account operators use this skill to discover relevant trending topics, generate structured articles, apply WeChat-oriented HTML formatting, and create drafts for publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish or schedule WeChat public-account content using configured account credentials. <br>
Mitigation: Require manual preview and approval before enabling scheduled or live publishing, and limit use to operators authorized to post for the account. <br>
Risk: The configuration includes a WeChat AppSecret and other account publishing settings. <br>
Mitigation: Keep AppSecret out of source control, restrict access to the configuration file, and rotate the secret if it is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andyy1976/wechat-publisher-3) <br>
- [Publisher profile](https://clawhub.ai/user/andyy1976) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with JSON configuration examples and WeChat-ready HTML/CSS content guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces publishing guidance and draft content; live WeChat publishing requires configured AppID, AppSecret, and manual review before scheduled or live use.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata); artifact frontmatter declares 1.0.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
