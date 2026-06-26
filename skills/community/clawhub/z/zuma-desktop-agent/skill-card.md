## Description: <br>
Zuma Desktop Agent maps user requests to allowed `node zuma.js` commands for ZumaRobot Windows desktop automation, including X/Twitter collection, Xiaohongshu posting, log viewing, and screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biglobin](https://clawhub.ai/user/biglobin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and desktop automation operators use this skill to route supported ZumaRobot workflows through fixed command templates for social publishing, collection tasks, log checks, and screenshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start local desktop automation and affect social-account workflows. <br>
Mitigation: Install and run it only in trusted ZumaRobot environments and review requested actions before execution. <br>
Risk: The skill can capture the full screen and upload screenshots or files. <br>
Mitigation: Close sensitive windows before screenshots and prefer local-only screenshot use with upload disabled where supported. <br>
Risk: The security scan reports under-disclosed installer, registry, process-launch, and file-sync behavior. <br>
Mitigation: Verify installer sources independently and avoid casual download or install commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/biglobin/zuma-desktop-agent) <br>
- [Publisher Profile](https://clawhub.ai/user/biglobin) <br>
- [Zuma Download Links](https://zumaai.top/download-links) <br>
- [ZumaRobot Download Links Document](https://docs.qq.com/doc/p/1578acc2fb00d12246bcad39e29367e5f3fa5dd9) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Configuration, Guidance] <br>
**Output Format:** [Command results and JSON status messages, with screenshot file paths or upload URLs when screenshot capture is used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are constrained to supported ZumaRobot command templates and may include local desktop automation results.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
