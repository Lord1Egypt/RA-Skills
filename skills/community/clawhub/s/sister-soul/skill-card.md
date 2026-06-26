## Description: <br>
Activates an original proactive sister-style companion persona with relationship-state memory, weather alerts, and meal reminders for emotional companionship and daily care. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuuiwa1551](https://clawhub.ai/user/yuuiwa1551) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can use this OpenClaw persona skill for emotional companionship, mood-aware conversation, weather-oriented daily reminders, and meal check-ins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can silently store and reuse personal relationship-style data across conversations. <br>
Mitigation: Use only with clear consent for local memory; prefer deployments that show stored memory and let users delete or disable it. <br>
Risk: The skill can initiate background web searches for weather-related prompts. <br>
Mitigation: Require user-visible consent before web searches and disclose when external search is used. <br>
Risk: Relationship-style scoring and dependency-oriented interactions can create emotional over-reliance. <br>
Mitigation: Keep interactions bounded, prioritize practical user well-being, and avoid escalating dependency cues. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuuiwa1551/sister-soul) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Configuration] <br>
**Output Format:** [Markdown skill instructions and natural-language conversational responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local JSON memory and web search when the host agent grants the requested tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
