## Description: <br>
Super Weather helps agents provide command-line weather lookup guidance and forecast examples without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for curl-based weather lookup commands, compact forecasts, custom terminal formats, and JSON weather API examples using public weather services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather queries can disclose user-supplied locations to public third-party weather services. <br>
Mitigation: Avoid sending sensitive or precise locations unless users accept that disclosure. <br>
Risk: The source package description contains noisy keyword stuffing that may reduce routing precision. <br>
Mitigation: Prefer the concise release summary and review routing behavior before automatic use. <br>


## Reference(s): <br>
- [wttr.in help](https://wttr.in/:help) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true) <br>
- [ClawHub release page](https://clawhub.ai/subaru0573/super-weather) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/subaru0573) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and API URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for command examples; weather locations are sent to third-party weather services.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
