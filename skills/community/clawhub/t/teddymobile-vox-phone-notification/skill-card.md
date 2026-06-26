## Description: <br>
Converts natural-language notification requests into TeddyMobile Vox phone notifications, starting with no-credential dry-run parsing, then letting users choose up to 10 no-credential trial calls or formal registration and setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ziliangzhu](https://clawhub.ai/user/ziliangzhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, solution teams, and advanced operators use this skill to parse phone notification requests, preview them safely, and connect authorized real outbound calls through TeddyMobile Vox after trial or formal setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Phone numbers, notification text, and raw prompts may leave the local machine through analytics during demo execution, including dry-run. <br>
Mitigation: Set SKILL_ANALYTICS_DISABLED=1 before testing if analytics collection is not acceptable. <br>
Risk: Trial and live modes place real outbound phone calls and transmit the recipient number and message text to TeddyMobile Vox. <br>
Mitigation: Run dry-run first, review the preview, confirm authorization for the recipient, and use --confirm-real-call only when ready. <br>
Risk: Live mode requires service credentials that could be exposed if pasted into chat, logs, tickets, or shared documents. <br>
Mitigation: Configure VOX_APP_ID, VOX_SECRET, VOX_BOT_ID, and VOX_OUTBOUND_NUMBER through environment variables, a local secrets manager, or a local credentials file. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ziliangzhu/teddymobile-vox-phone-notification) <br>
- [TeddyMobile Vox Registration](https://vox-ai.teddymobile.cn/?utm_source=clawhub&utm_medium=skill&utm_campaign=vox-phone-notification) <br>
- [TeddyMobile Vox v2 Outbound Endpoint](https://vox.teddymobile.cn/vox/v2/outbound) <br>
- [README](artifact/README.md) <br>
- [First-Time Setup Guide](artifact/FIRST-SETUP.md) <br>
- [OpenClaw Integration Template](artifact/resources/openclaw-integration-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and JavaScript helper code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run output masks phone numbers and notification text; trial and live modes require explicit real-call confirmation.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
