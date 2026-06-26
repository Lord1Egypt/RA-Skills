## Description: <br>
Get current weather and forecasts (no API key required). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agents use this skill to look up current weather and forecasts through public weather services without managing API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Precise home coordinates or similarly sensitive locations may be shared with public weather services during lookups. <br>
Mitigation: Use city names, airport codes, or approximate locations when precise coordinates are not necessary. <br>
Risk: Weather responses depend on public services and may be unavailable, delayed, or inaccurate. <br>
Mitigation: Use the documented fallback service and verify important weather decisions with an authoritative local source. <br>


## Reference(s): <br>
- [wttr.in help](https://wttr.in/:help) <br>
- [Open-Meteo documentation](https://open-meteo.com/en/docs) <br>
- [Weather on ClawHub](https://clawhub.ai/steipete/weather) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with bash code blocks and weather API URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for command examples; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
