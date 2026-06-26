## Description: <br>
Tencent Map Location Services helps agents search POIs, find nearby places, plan routes and trips, and create map or trajectory visualizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-adm](https://clawhub.ai/user/tencent-adm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to answer location-service requests with Tencent Maps data, including nearby search, POI search, route planning, travel planning, and trajectory visualization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prompt for or persist Tencent Maps API keys when triggered too broadly. <br>
Mitigation: Use an environment variable or secret manager for production keys, and confirm explicitly before allowing tmap-lbs config set-key to persist a key. <br>
Risk: Generated trajectory map links may expose private, internal, signed, or sensitive trajectory-data URLs. <br>
Mitigation: Avoid using sensitive trajectory-data URLs in generated map links and review shared links before sending them to users. <br>


## Reference(s): <br>
- [Scene 1: Nearby Search](tencentmap-lbs-skill/references/scene1-nearby-search.md) <br>
- [Scene 2: POI Search](tencentmap-lbs-skill/references/scene2-poi-search.md) <br>
- [Scene 3: Route Planning](tencentmap-lbs-skill/references/scene3-route-planning.md) <br>
- [Scene 4: Travel Planner](tencentmap-lbs-skill/references/scene4-travel-planner.md) <br>
- [Scene 5: Trail Map](tencentmap-lbs-skill/references/scene5-trail-map.md) <br>
- [Tencent Location Service](https://lbs.qq.com/) <br>
- [Tencent Maps Web Service API Overview](https://lbs.qq.com/service/webService/webServiceGuide/webServiceOverview) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, API call guidance] <br>
**Output Format:** [Markdown with inline shell commands, generated map links, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require the tmap-lbs CLI and TMAP_WEBSERVICE_KEY for production Tencent Maps requests.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
