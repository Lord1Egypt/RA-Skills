## Description: <br>
Get current weather and forecasts with wttr.in and Open-Meteo without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[99percentgod](https://clawhub.ai/user/99percentgod) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to fetch current conditions, compact weather summaries, full forecasts, and machine-readable weather JSON for user-specified locations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather lookups make outbound requests to public weather services, which can reveal queried locations to those services. <br>
Mitigation: Use only locations needed for the task, avoid sensitive personal addresses when privacy matters, and review network access policies before deployment. <br>
Risk: The skill can write requested weather output files, such as PNG forecasts. <br>
Mitigation: Choose explicit output paths, avoid overwriting important files, and review generated files before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/99percentgod/weather-1-0-0) <br>
- [wttr.in help](https://wttr.in/:help) <br>
- [Open-Meteo documentation](https://open-meteo.com/en/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with curl commands; weather responses may be plain text, JSON, or PNG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
