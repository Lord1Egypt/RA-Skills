## Description: <br>
Helps agents plan travel itineraries, create valid trip-packer JSON, run the CLI, and deliver local HTML map pages with optional share images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ucasytoo](https://clawhub.ai/user/ucasytoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel planners and agents use this skill to turn destination, hotel, route, and activity details into validated itinerary JSON and a shareable local map artifact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may run npx trip-packer, which depends on the npm package resolved at execution time. <br>
Mitigation: Pin or verify the trip-packer npm package before use when supply-chain control matters. <br>
Risk: Generated map artifacts and third-party map tile requests can expose sensitive travel, hotel, or location details. <br>
Mitigation: Avoid including sensitive itinerary details, review generated files before sharing, and consider map tile exposure when choosing what to publish. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ucasytoo/trip-packer) <br>
- [Trip Packer Planning Guide](planning-guide.md) <br>
- [trip-packer JSON Schema Reference](references/schema-reference.md) <br>
- [Sample Itinerary JSON](references/sample-itinerary.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, JSON, HTML, Images, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with JSON itinerary files, npx trip-packer commands, local HTML map files, and optional PNG image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and uses npx trip-packer; no credential environment variables are declared.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
