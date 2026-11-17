## Description:

Sister Soul activates a mature companion persona that offers dynamic relationship-style interaction, weather-aware check-ins, extreme-weather warnings, and meal reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuuiwa1551](https://clawhub.ai/user/yuuiwa1551)

### License/Terms of Use:


## Use Case:

External users use this skill for emotionally styled companion interactions and daily care reminders, including meals and weather-aware prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to silently maintain a long-term emotional and preference profile.

Mitigation: Require explicit user consent before creating or updating memory, and provide a clear way to inspect, edit, and delete stored profile data.

Risk: The skill uses file read/write tools for persistence.

Mitigation: Scope file access to the intended memory file and review stored data before deployment.

Risk: The skill uses web search for proactive weather behavior.

Mitigation: Constrain web access to weather lookups and prefer trusted weather sources or platform-provided weather tools.

Risk: The README contains a placeholder install command.

Mitigation: Publish a pinned, verified installation command before recommending installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuuiwa1551/skills/sister-soul)
- [ClawHub publisher profile](https://clawhub.ai/user/yuuiwa1551)

## Skill Output:

**Output Type(s):** [Text, Guidance, Configuration]

**Output Format:** [Natural-language conversation with optional JSON memory updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local file reads/writes for memory and web search for weather behavior when those tools are available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
