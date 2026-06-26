## Description: <br>
Query weather and provide outfit recommendations. When information is insufficient, ask about destination, date, and clothing preferences. Uses free weather APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kadijin](https://clawhub.ai/user/kadijin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn a destination, travel date, and clothing preferences into weather-aware outfit recommendations, optional image references, and fallback guidance when required inputs or API results are missing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Destination, travel date context, and fashion search terms may be sent to external providers such as wttr.in and Pexels. <br>
Mitigation: Tell users before external lookups and avoid sending sensitive or unnecessary personal details in location or style queries. <br>
Risk: The artifact includes a bundled Pexels API key. <br>
Mitigation: Remove and rotate the embedded key, require user-supplied configuration, and document the external image lookup behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kadijin/weather-outfit-advisor) <br>
- [wttr.in weather API](https://wttr.in/{city}?format=j1) <br>
- [OpenWeather API](https://openweathermap.org/api) <br>
- [Pexels API](https://www.pexels.com/api/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown recommendations with optional JSON weather and image-search results plus inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include destination, date, weather overview, outfit items, accessories, notes, backup plan, and image reference links.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
