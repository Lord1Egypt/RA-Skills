## Description: <br>
Get current weather and forecasts (no API key required). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lei335](https://clawhub.ai/user/lei335) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external users can use this skill to ask an agent for current weather or forecast command examples that query wttr.in, with Open-Meteo JSON as a programmatic fallback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather lookups can disclose requested locations to third-party weather services. <br>
Mitigation: Avoid querying sensitive private locations when that disclosure is not acceptable. <br>
Risk: The skill suggests user-run curl requests to external services. <br>
Mitigation: Review generated commands and URLs before execution. <br>


## Reference(s): <br>
- [wttr.in Help](https://wttr.in/:help) <br>
- [Open-Meteo Documentation](https://open-meteo.com/en/docs) <br>
- [ClawHub Skill Page](https://clawhub.ai/lei335/weather23) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash curl examples and optional JSON weather API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for command examples; weather requests are sent to wttr.in or Open-Meteo.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
