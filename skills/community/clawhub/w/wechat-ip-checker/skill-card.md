## Description: <br>
Checks the current public IP with ip38.com, compares it with a configured WeChat publishing IP, and gates WeChat article publishing on the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[achievejia](https://clawhub.ai/user/achievejia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers or operators who publish WeChat public-account articles use this skill to verify the machine's public IP against a configured whitelist record before invoking the dependent publishing skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can lead to public WeChat publishing without a clearly required final approval step. <br>
Mitigation: Require explicit confirmation that shows the WeChat account, article, and publish-or-draft action before invoking the publishing skill. <br>
Risk: The actual account action is performed by the separate baoyu-post-to-wechat skill. <br>
Mitigation: Review and approve the dependent publishing skill separately before using this workflow. <br>
Risk: A stale or incorrect local public-IP record can block publishing or prompt an unsafe whitelist update. <br>
Mitigation: Verify the configured IP record and update it only after confirming the matching whitelist entry in the WeChat public platform. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/achievejia/wechat-ip-checker) <br>
- [ip38.com public IP lookup](https://www.ip38.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions and status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke browser-based IP lookup and a dependent WeChat publishing skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
