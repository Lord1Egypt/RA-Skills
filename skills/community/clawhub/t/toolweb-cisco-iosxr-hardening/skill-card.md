## Description: <br>
Generate security hardening configurations for Cisco IOS XR devices with customizable hardening options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network administrators, security teams, and infrastructure automation engineers use this skill to request repeatable Cisco IOS XR hardening configuration snippets for review, audit, and deployment planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Cisco IOS XR configuration could disrupt live routing, access, authentication, logging, or service behavior if applied without review. <br>
Mitigation: Review and lab-test generated AAA, SSH, ACL, logging, and service-shutdown changes before deploying them to production routers. <br>
Risk: Requests to the third-party API may expose sensitive network context or device secrets if users include them in prompts or parameters. <br>
Mitigation: Do not submit real device secrets or sensitive production details unless the provider and its data handling have been approved. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-cisco-iosxr-hardening) <br>
- [Cisco IOS XR Hardening API Docs](https://api.mkkpro.com:8138/docs) <br>
- [Cisco IOS XR Hardening API Route](https://api.mkkpro.com/hardening/cisco-iosxr) <br>
- [ToolWeb](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, JSON, guidance] <br>
**Output Format:** [JSON API responses containing generated Cisco IOS XR configuration snippets, applied options, and warnings when available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires hardeningOptions, sessionId, and timestamp; generated configurations should be reviewed and lab-tested before use on live routers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
