## Description: <br>
Plan multi-day road trip routes in mainland China using Amap APIs, generate continuous-route personal map QR codes, and produce daily itinerary details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlydreams](https://clawhub.ai/user/onlydreams) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and agents use this skill to design multi-day mainland China road trips with controlled daily driving time, route continuity, supply-point checks, and Amap personal-map QR output. <br>

### Deployment Geography for Use: <br>
Mainland China <br>

## Known Risks and Mitigations: <br>
Risk: Planned route locations are sent to Amap APIs during geocoding, POI search, route planning, and map generation. <br>
Mitigation: Use the skill only when sharing planned route locations with Amap is acceptable for the user and organization. <br>
Risk: The skill requires an Amap API key and a dependent personal-map skill. <br>
Mitigation: Configure AMAP_API_KEY through the environment, avoid exposing the key in prompts or logs, and confirm the installed personal-map dependency is the intended one before use. <br>
Risk: The skill may create or overwrite /tmp/road_trip_qr.png. <br>
Mitigation: Treat the QR image as temporary output and move or rename any existing file that must be preserved before running the workflow. <br>


## Reference(s): <br>
- [Road Trip Planner on ClawHub](https://clawhub.ai/onlydreams/road-trip-planner) <br>
- [@lbs-amap/personal-map dependency](https://clawhub.ai/lbs-amap/personal-map) <br>
- [Amap Open Platform](https://lbs.amap.com/) <br>
- [Examples](examples.md) <br>
- [Seasonal checklist](references/seasonal.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown itinerary with tables, inline shell setup guidance, route links, and a local QR image reference when generated] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or overwrite /tmp/road_trip_qr.png during use.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
