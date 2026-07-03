## Description: <br>
Get real-time commute traffic using TomTom Routing API. Live travel times, delays, and ETAs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vijays365](https://clawhub.ai/user/vijays365) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve real-time commute distance, travel time, traffic delay, and ETA data from the TomTom Routing API. It can also support scheduled commute notifications when combined with the optional AgentMail example. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Precise commute locations and optional departure timing are sent to TomTom. <br>
Mitigation: Use the skill only when sharing those route details with TomTom is acceptable, and avoid entering unnecessary personal location details. <br>
Risk: Crafted input values may cause unintended local Python code execution in the shell scripts. <br>
Mitigation: Use trusted route, name, and email inputs only until the scripts pass values safely into Python instead of interpolating them into source code. <br>
Risk: The optional AgentMail example uses additional email credentials and sends commute information to an external email service. <br>
Mitigation: Enable the email workflow only with trusted AgentMail configuration and intended recipients. <br>


## Reference(s): <br>
- [TomTom Developer Portal](https://developer.tomtom.com/) <br>
- [TomTom Routing API calculateRoute endpoint](https://api.tomtom.com/routing/1/calculateRoute/{origin}:{dest}/json) <br>
- [AgentMail send message endpoint](https://api.agentmail.to/v0/inboxes/${AGENTMAIL_INBOX}/messages/send) <br>
- [ClawHub skill page](https://clawhub.ai/vijays365/tomtom-traffic-commute) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON from the traffic script, with Markdown setup and usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOMTOM_API_KEY plus curl and bash; the optional email workflow can use AgentMail credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
