## Description: <br>
Automates Windows PC WeChat via pywinauto UI automation for messages, files, Moments, contacts, and related workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hello-mr-crab](https://clawhub.ai/user/hello-mr-crab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to generate and run Python/pywinauto scripts that automate a logged-in Windows PC WeChat client for messaging, files, contacts, Moments, and settings workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes broad control over a logged-in Windows WeChat client, including account-changing and data-access actions. <br>
Mitigation: Restrict agents to explicit user-requested actions and require confirmation before sending, posting, accepting contacts, joining groups, clearing history, changing settings, or scheduling tasks. <br>
Risk: Exported chats, contacts, QR codes, local WeChat paths, files, and media may contain private data. <br>
Mitigation: Treat these outputs as sensitive, minimize retention, and avoid sharing or logging them unless the user explicitly requests it. <br>
Risk: Frequent automated actions may disrupt the WeChat session or violate WeChat usage expectations. <br>
Mitigation: Use conservative delays, stop on automation errors instead of retrying automatically, and operate only within the user's intended and permitted activity. <br>


## Reference(s): <br>
- [Pyweixin RPA on ClawHub](https://clawhub.ai/hello-mr-crab/pyweixin-rpa) <br>
- [pyweixin RPA API Reference](references/api_reference.md) <br>
- [Weixin 4.1+ UI Automation Notes](references/Weixin4.0.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Windows-only automation for a local logged-in WeChat client; outputs may trigger UI actions when executed.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and metadata.openclaw.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
