## Description: <br>
Daily weather briefing for any city - morning conditions, what to wear, umbrella forecast, evening preview, extreme weather alerts. No API key. Works worldwide. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiajiaoy](https://clawhub.ai/user/jiajiaoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to generate practical weather briefings, umbrella and clothing advice, weekly or monthly forecasts, and optional recurring weather notifications for a configured city. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Enabling recurring pushes stores local preferences such as user ID, city, units, timing, timezone, channel, and push status. <br>
Mitigation: Use the status and off commands to review or disable push settings, and avoid putting sensitive personal data into user IDs or city labels. <br>
Risk: Weather results depend on real-time web search and should not be treated as official emergency alerts. <br>
Mitigation: Verify severe-weather decisions with official meteorological or emergency-management sources before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiajiaoy/weather-daily) <br>
- [README.md](README.md) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown and plain text prompts, with shell commands for registration and push management.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-generator scripts may also emit OpenClaw cron add/remove control messages for recurring notifications.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
