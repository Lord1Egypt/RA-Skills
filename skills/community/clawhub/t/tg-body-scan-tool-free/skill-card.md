## Description: <br>
This skill helps individual users submit body-scan videos through Telegram and receive basic circumference measurements plus a waist-to-hip ratio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External personal fitness users use this skill to submit consenting body-scan videos through Telegram for one-off body measurement, waist-to-hip ratio review, and manual health-record tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive body videos and body measurements may expose private biometric or health-adjacent information. <br>
Mitigation: Use the skill only with informed user consent, avoid scanning other people without explicit permission, and clarify retention and deletion practices before installation. <br>
Risk: Telegram bot tokens and scanning-service credentials could be mishandled if placed in prompts, files, or logs. <br>
Mitigation: Store credentials only in secure agent or platform configuration and avoid embedding secrets in skill text, examples, or conversation history. <br>
Risk: Body measurements and waist-to-hip ratio guidance may be inaccurate or mistaken for medical advice. <br>
Mitigation: Treat outputs as fitness-tracking references, repeat measurements under consistent conditions, and consult qualified professionals for health decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/tg-body-scan-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls, Guidance] <br>
**Output Format:** [Telegram-style text responses and JSON result objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include scan status, circumference measurements, waist-to-hip ratio, execution logs, and error details.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
