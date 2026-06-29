## Description: <br>
Guides agents through creating, repairing, and validating local macOS clone apps for WeChat and WeCom so users can run a second local login window. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ipythoning](https://clawhub.ai/user/ipythoning) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to guide safe, local-only cloning of installed WeChat or WeCom macOS app bundles, including bundle identity changes, re-signing, troubleshooting, and validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local app cloning and re-signing can break cloned Tencent apps or create confusing duplicate bundles after updates. <br>
Mitigation: Work only on the user's own Mac and already installed apps, keep backups, avoid modifying the original applications, and revalidate the clone after app updates. <br>
Risk: Local bundle identity isolation cannot bypass vendor account or device policies. <br>
Mitigation: Set expectations before troubleshooting and report likely service-side policy limits when the same account cannot remain logged in across both clients. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ipythoning/wechat-wecom-macos-clones) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell command blocks and validation checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local macOS workflow guidance only; no API calls or network services are required by the skill.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
