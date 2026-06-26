## Description: <br>
Tabussen helps agents plan Västerbotten and Umeå public transport journeys using the ResRobot API, including stops, addresses, coordinates, regional routes, and local routes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Simskii](https://clawhub.ai/user/Simskii) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent operators use Tabussen to find stops and plan bus, train, and walking journeys in Västerbotten, especially around Umeå local and regional public transport. <br>

### Deployment Geography for Use: <br>
Sweden <br>

## Known Risks and Mitigations: <br>
Risk: Trip searches and location queries are sent to the ResRobot service. <br>
Mitigation: Use the skill only when users are comfortable sharing the requested trip details with ResRobot. <br>
Risk: The skill requires a ResRobot/Trafiklab API key. <br>
Mitigation: Use a dedicated API key, provide it through RESROBOT_API_KEY, and keep it out of shared logs. <br>
Risk: The scripts depend on local curl and jq installations. <br>
Mitigation: Confirm curl and jq are installed before using the search and journey scripts. <br>


## Reference(s): <br>
- [Tabussen ClawHub release](https://clawhub.ai/Simskii/tabussen) <br>
- [ResRobot API](https://api.resrobot.se/v2.1/) <br>
- [ResRobot trip endpoint](https://api.resrobot.se/v2.1/trip) <br>
- [ResRobot location endpoint](https://api.resrobot.se/v2.1/location.name) <br>
- [Trafiklab developer portal](https://developer.trafiklab.se) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown responses with shell command examples and plain-text journey results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and a RESROBOT_API_KEY environment variable; trip searches are sent to ResRobot.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
