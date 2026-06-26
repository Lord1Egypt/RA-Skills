## Description: <br>
Find nearby Wikipedia articles based on geographic location. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jrrqd](https://clawhub.ai/user/jrrqd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn a shared location, coordinates, or place name into nearby Wikipedia articles with distances and optional brief descriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Precise location data can reveal sensitive places when used with browser geolocation or API queries. <br>
Mitigation: Use an approximate place name or ask the agent to confirm before sending exact coordinates for sensitive locations. <br>
Risk: Nearby results may be sparse or empty where Wikipedia has few geotagged articles. <br>
Mitigation: Set expectations, try a broader radius when appropriate, or ask for a nearby known place as the search center. <br>


## Reference(s): <br>
- [Wikipedia Nearby](https://en.wikipedia.org/wiki/Special:Nearby) <br>
- [Wikipedia API endpoint](https://en.wikipedia.org/w/api.php) <br>
- [ClawHub skill page](https://clawhub.ai/jrrqd/wikipedia-nearby) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with URL templates, nearby-article summaries, and optional curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided coordinates, browser geolocation permission, or a geocoded place name; results depend on Wikipedia articles with geographic coordinates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
