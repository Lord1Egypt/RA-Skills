## Description: <br>
Launches a personalized AI wellness coach video session using Tavus CVI and Claude, with optional wearable health data, Google Calendar context, wellness recommendations, and Telegram briefing delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andrechuabio](https://clawhub.ai/user/andrechuabio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to start a personalized morning wellness coaching flow that combines wearable health metrics, calendar events, Claude-generated recommendations, a Tavus video session, and optional Telegram delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process private wearable health metrics, calendar summaries, and video session links through configured external services. <br>
Mitigation: Install and run it only after reviewing the data flows, API-key configuration, and service destinations, and only with accounts the user intends to connect. <br>
Risk: Scheduled Telegram delivery can send personal briefing content or session links to the wrong destination if reused without changes. <br>
Mitigation: Replace the recipient, agent name, and delivery target with a verified destination before enabling the cron workflow. <br>
Risk: A broad HEARTBEAT forwarding rule can cause an agent to forward content with limited contextual checks. <br>
Mitigation: Use a narrow, reviewable automation rule and confirm how to disable the daily cron before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andrechuabio/wellness-coach) <br>
- [Google Calendar setup](references/gcal-setup.md) <br>
- [OpenClaw cron setup](references/openclaw-cron.md) <br>
- [Wearable integration guide](references/wearables.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with setup steps, shell commands, endpoint descriptions, and briefing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live Tavus session links and Telegram briefing content when configured by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
