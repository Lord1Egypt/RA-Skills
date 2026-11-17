## Description: <br>
Weather Toolkit Free helps agents answer current-weather and short forecast requests using wttr.in and Open-Meteo without API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to look up current weather, a three-day forecast, and script-friendly weather output for a single location. It is intended for weather queries, command-line examples, and lightweight workflow integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill metadata may cause agents to consider it for database or SQL tasks even though it is a weather lookup guide. <br>
Mitigation: Use the skill only for weather queries and disregard database or SQL activation language. <br>
Risk: Weather lookup commands can send city names, airport codes, or coordinates to wttr.in or Open-Meteo. <br>
Mitigation: Avoid sending sensitive locations, and review command examples before running them. <br>
Risk: The skill declares command and write access while providing examples that can execute shell commands or save weather output files. <br>
Mitigation: Review proposed commands and file paths before execution, especially commands that write output such as PNG exports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/weather-toolkit-free) <br>
- [Skill homepage](https://skillhub.cn) <br>
- [wttr.in weather endpoint](https://wttr.in/{city}) <br>
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, Python snippets, and optional JSON weather responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call wttr.in or Open-Meteo when command examples are executed; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
