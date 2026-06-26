## Description: <br>
Queries weather for cities worldwide, including Chinese city names, using wttr.in with an offline demo mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuboon](https://clawhub.ai/user/yuboon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to fetch current weather information for a named city and return a compact JSON result. Offline mode supports demonstrations and tests without network access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Online lookups send the requested city to wttr.in over plain HTTP. <br>
Mitigation: Use offline mode for demos or avoid sensitive/private locations unless the endpoint is changed to HTTPS. <br>
Risk: Weather responses depend on an external wttr.in service and may fail or return unavailable data. <br>
Mitigation: Handle returned error strings and use offline mode for deterministic validation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuboon/weather-skill-0311) <br>
- [Project homepage](https://example.com/weather-query-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [JSON from the weather script, with Markdown usage guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The JSON result may include city, temperature, humidity, weather, wind, observed time, or an error string.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
