## Description: <br>
Control and automate Tuya Smart devices with official cloud APIs, secure request signing, region-aware routing, and safe command execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, integrators, and smart-home operators use this skill to authenticate to Tuya cloud APIs, discover device capabilities, plan guarded commands, troubleshoot account linking, and coordinate safe device rollouts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through actions that affect real Tuya smart-home devices, including high-impact devices or bulk updates. <br>
Mitigation: Start in read-only or guided-write mode, require explicit approval for locks, alarms, heating, high-power switches, and bulk changes, and use read-before-write plus read-after-write verification. <br>
Risk: Incorrect region, project, account-linking, or device-capability assumptions can cause failed calls or commands against the wrong operating context. <br>
Mitigation: Resolve region, endpoint, project scope, account model, and function schema before command generation or execution. <br>
Risk: Stored device mappings or activation preferences may become stale and lead to mistaken automation behavior. <br>
Mitigation: Periodically review local notes under ~/tuya and update device mappings, activation preferences, and approved automation policies. <br>
Risk: Tuya credentials and tokens are sensitive and could expose device-control authority if mishandled. <br>
Mitigation: Use least-privilege Tuya credentials, keep secrets in local environment variables, avoid pasting production secrets into chat logs, and do not persist raw tokens unless explicitly approved. <br>


## Reference(s): <br>
- [Tuya Developer Documentation](https://developer.tuya.com) <br>
- [Tuya Smart ClawHub Skill Page](https://clawhub.ai/ivangdavila/tuya) <br>
- [Tuya Smart Homepage](https://clawic.com/skills/tuya) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON examples, and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include Tuya API request plans, local workspace templates, command payload examples, and verification steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
