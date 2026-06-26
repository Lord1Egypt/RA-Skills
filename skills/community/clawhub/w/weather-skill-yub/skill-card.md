## Description: <br>
Queries weather for cities worldwide, including Chinese city names, using wttr.in with an offline sample mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuboon](https://clawhub.ai/user/yuboon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to look up current weather for a specified city and return structured weather details. The offline mode supports local validation without making a network request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Online city lookups are sent to wttr.in over plain HTTP. <br>
Mitigation: Avoid sensitive location queries in online mode, or use offline mode when external requests are not acceptable. <br>
Risk: The documented install command appears to use a placeholder package name. <br>
Mitigation: Verify the ClawHub package name and publisher handle before installing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuboon/weather-skill-yub) <br>
- [Project homepage](https://example.com/weather-query-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [JSON weather data from the helper script, plus Markdown usage guidance in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [City name input; optional offline mode for sample output] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
