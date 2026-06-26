## Description: <br>
A self-drive travel roadbook toolkit for creating and updating trip roadbooks, archiving photos, generating Leaflet and OSRM route maps, and producing HTML or PDF roadbooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ffsszzll](https://clawhub.ai/user/ffsszzll) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and agents use this skill to maintain self-drive trip roadbooks, organize day-by-day notes and photos, enrich route stops with elevation data, and generate maps and printable trip documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit local roadbook Markdown and write generated trip files to hardcoded paths. <br>
Mitigation: Back up the roadbook before running scripts and review path settings before generation. <br>
Risk: Route and elevation generation can send place names or coordinates to external map and elevation services. <br>
Mitigation: Avoid automatic generation for sensitive trips unless sharing those locations with the listed services is acceptable. <br>
Risk: Generated maps, elevations, and route details may be incomplete or inaccurate because they depend on third-party services and configured place data. <br>
Mitigation: Review generated routes, elevation values, and printable outputs before using them for travel planning or publication. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ffsszzll/ravel-roadbook) <br>
- [OSRM public routing endpoint](https://router.project-osrm.org/route/v1/driving/) <br>
- [Nominatim search endpoint](https://nominatim.openstreetmap.org/search?q={name}&format=json&limit=1) <br>
- [Open-Elevation lookup endpoint](https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell and Python commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local roadbook Markdown, HTML/PDF generation guidance, route-map files, and elevation lookup updates depending on the workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
