## Description:

Search the Recreation Information Database (RIDB) for campgrounds, recreation areas, and federal facilities near a location using city geocoding or latitude/longitude coordinates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanrea](https://clawhub.ai/user/seanrea)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to discover federal campgrounds and recreation facilities near a destination, retrieve campground IDs and facility metadata, and produce JSON for downstream availability workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location-name queries are sent to OpenStreetMap/Nominatim and campsite search coordinates are sent to RIDB.

Mitigation: Avoid entering home addresses or other sensitive exact locations; use latitude/longitude coordinates when they are sufficient.

Risk: Passing the RIDB API key on the command line can expose it through shell history or local process listings.

Mitigation: Set RIDB_API_KEY in the environment instead of using the --api-key flag.

## Reference(s):

- [RIDB API Notes](references/api-notes.md)
- [RIDB Portal](https://ridb.recreation.gov)
- [RIDB API Key Profile](https://ridb.recreation.gov/profile)
- [recreation.gov](https://www.recreation.gov)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI examples; the CLI can emit human-readable text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a RIDB API key; location-name searches use OpenStreetMap/Nominatim geocoding.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
