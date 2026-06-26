## Description: <br>
Provides weather, dictionary, Wikipedia, writing, workout, web search, weight tracking, and hydration reminder utilities through a Python skill pack. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hgta23](https://clawhub.ai/user/hgta23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this Python utility pack to answer daily information requests, get lightweight writing or workout guidance, and maintain in-memory wellness reminders or logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather, search, wiki, dictionary, health, and location inputs may be sent to external services. <br>
Mitigation: Avoid entering sensitive health or location details unless needed, and review third-party service use before deployment. <br>
Risk: The weather call uses HTTP in the artifact source. <br>
Mitigation: Change the OpenWeatherMap request to HTTPS before using a real API key. <br>
Risk: API keys are represented as source placeholders. <br>
Mitigation: Provide real keys through a secret manager or environment configuration rather than hardcoding them in source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hgta23/w) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Plain text strings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include search snippets, weather summaries, generated workout plans, and in-memory tracking summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
