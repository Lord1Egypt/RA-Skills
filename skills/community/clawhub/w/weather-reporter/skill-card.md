## Description: <br>
Generates weather report images for a chosen city with weather charts, AI-generated background art, and concise weather tips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zyt64](https://clawhub.ai/user/zyt64) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run a Python weather-report generator for cities worldwide. It produces a visual weather summary with temperature, precipitation, humidity, wind, sunrise/sunset, moon phase, UV index, and short AI-generated tips. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends city and weather-derived data to wttr.in, ZhipuAI, and the configured OpenAI-compatible LLM provider. <br>
Mitigation: Install only when those external data flows are acceptable for the intended use case. <br>
Risk: API keys are stored in config.json for ZhipuAI and the configured LLM provider. <br>
Mitigation: Keep config.json private and do not commit or share real API keys. <br>
Risk: The tool deletes and overwrites fixed PNG filenames such as 1.png, bg.png, make.png, and output.png. <br>
Mitigation: Run it in a dedicated folder so unrelated image files are not overwritten or removed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zyt64/weather-reporter) <br>
- [wttr.in weather data service](https://wttr.in/) <br>
- [Zhipu AI platform](https://open.bigmodel.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Images, Shell commands, Configuration] <br>
**Output Format:** [PNG image file plus command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes output.png and temporary PNG files in the working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
