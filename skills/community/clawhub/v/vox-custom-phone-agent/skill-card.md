## Description: <br>
Converts natural-language phone tasks into structured TeddyMobile Vox custom-bot outbound calls with guided missing-field collection, safety checks, voice selection, and trial or formal account modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ziliangzhu](https://clawhub.ai/user/ziliangzhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure and run a Vox phone-agent flow that gathers call intent, validates required details, selects a voice, and starts a trial or formal outbound call. It is intended for guided customer notification, appointment, follow-up, and similar business phone workflows. <br>

### Deployment Geography for Use: <br>
Global, subject to local outbound calling, AI disclosure, privacy, and consent requirements. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real outbound phone calls. <br>
Mitigation: Require explicit user confirmation before calls, enforce quotas and abuse controls, and use trial or formal account permissions only where authorized. <br>
Risk: AI identity, call-recipient consent, and local phone-call rules may be under-scoped. <br>
Mitigation: Confirm disclosure, consent, and recording/transcript practices with legal and business owners before use in each jurisdiction. <br>
Risk: Prompt, usage telemetry, call results, or transcripts may be sent, retrieved, or forwarded. <br>
Mitigation: Use hosted mode with your own authentication, minimize or disable analytics where possible, mask phone numbers, and define transcript retention and access controls. <br>
Risk: Formal Vox credentials enable production outbound-call access. <br>
Mitigation: Keep VOX_SECRET on a backend service, avoid publishing real credentials, and restrict access by authentication, IP allowlists, and audit logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ziliangzhu/vox-custom-phone-agent) <br>
- [GET_STARTED.md](artifact/GET_STARTED.md) <br>
- [FIRST_SETUP.md](artifact/FIRST_SETUP.md) <br>
- [REGISTRATION_GUIDE.md](artifact/REGISTRATION_GUIDE.md) <br>
- [Vox enterprise trial application](https://vox-ai.teddymobile.cn/trial/apply) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown/user-facing text with JSON-compatible status objects, configuration snippets, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate real Vox outbound calls when required fields, safety checks, and trial or formal account configuration are complete.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
