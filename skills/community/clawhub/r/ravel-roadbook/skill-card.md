## Description:

A self-drive travel roadbook toolkit for creating and updating trip notes, organizing photos, generating Leaflet and OSRM route maps, and producing printable HTML or PDF roadbooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ffsszzll](https://clawhub.ai/user/ffsszzll)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to maintain structured self-drive trip roadbooks, archive trip photos, enrich entries with elevation data, generate route maps, and prepare printable travel records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel locations are sent to public mapping and elevation services.

Mitigation: Use the skill only for trips whose locations may be shared with OSRM, Nominatim, Open-Elevation, Amap tile servers, and the Leaflet CDN.

Risk: Generated roadbook files and photo archives may store personal travel details on local disk.

Mitigation: Review and adjust hard-coded output paths before use, and store outputs only in directories appropriate for the trip data.

Risk: Generated HTML built from untrusted roadbook text or filenames could be unsafe to open.

Mitigation: Use trusted roadbook content and filenames, and review generated HTML before opening or converting it.

Risk: PDF or screenshot generation uses Chrome with --no-sandbox.

Mitigation: Remove the --no-sandbox option before relying on PDF or screenshot generation in normal use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ffsszzll/skills/ravel-roadbook)
- [OSRM route service endpoint](https://router.project-osrm.org/route/v1/driving/)
- [OpenStreetMap Nominatim search endpoint](https://nominatim.openstreetmap.org/search)
- [Open-Elevation lookup endpoint](https://api.open-elevation.com/api/v1/lookup)
- [Leaflet distribution CDN](https://unpkg.com/leaflet@1.9.4/dist/leaflet.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated local files such as HTML, PDF, route cache JSON, and updated roadbook Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces travel planning artifacts that may contain personal locations, photos, trip dates, lodging details, and expenses.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
