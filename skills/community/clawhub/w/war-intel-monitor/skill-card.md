## Description: <br>
Real-time war intelligence monitoring and emergency alert system for conflict zones. Use when user needs to track military conflicts, receive emergency alerts, monitor evacuation options, or assess safety risks during wartime situations. Supports customizable location-based threat assessment with distance calculations to military targets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OliviaPp8](https://clawhub.ai/user/OliviaPp8) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and safety-focused operators use this skill to monitor conflict-related news, assess location-based threats, prepare emergency alerts, and track evacuation options during wartime situations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for sensitive conflict-zone location, shelter, evacuation, and emergency-contact data. <br>
Mitigation: Use coarse locations where possible, keep configuration files out of synced folders and repositories, and restrict file access. <br>
Risk: Recurring monitoring and external alerts can expose sensitive alert payloads or continue longer than intended. <br>
Mitigation: Redact alert payloads before sending them to messaging services and set an end date or shutdown plan for cron jobs. <br>
Risk: Conflict monitoring output can be incomplete, delayed, or misleading for personal safety decisions. <br>
Mitigation: Treat generated briefings as supplemental information and rely on official local emergency, civil aviation, and embassy alerts for safety decisions. <br>


## Reference(s): <br>
- [Quick Setup Guide](references/setup-guide.md) <br>
- [Config Template](references/config-template.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/OliviaPp8/war-intel-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefings and alerts with optional shell commands and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include location-distance estimates, alert levels, emergency action lists, evacuation options, and cron monitoring schedules.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
