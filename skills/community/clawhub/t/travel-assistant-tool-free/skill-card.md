## Description: <br>
Travel Assistant Tool Free helps personal travelers organize trip details, check passport and visa timing, retrieve basic weather guidance, and generate packing and destination-preparation reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External personal travelers use this skill before a single-destination trip to organize dates, tickets, lodging tasks, documents, weather-driven clothing choices, packing needs, and culture or legal reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may request shell or network access for weather checks. <br>
Mitigation: Run it with the narrowest available tool scope, review proposed commands before execution, and avoid enabling exec unless live weather checks are needed. <br>
Risk: The skill asks for write access while the evidence notes contradictory export behavior and the artifact says free output is conversation-only. <br>
Mitigation: Treat file export as unsupported for this release and do not grant write permissions unless the publisher clarifies the expected behavior. <br>
Risk: Travel, visa, entry, weather, culture, and legal guidance can be incomplete or stale. <br>
Mitigation: Use the skill for planning prompts and checklists, then verify official government, carrier, lodging, and weather sources before travel. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/travel-assistant-tool-free) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and JSON-like structured responses with occasional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language conversational output; weather checks may use public web APIs when tool access is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
