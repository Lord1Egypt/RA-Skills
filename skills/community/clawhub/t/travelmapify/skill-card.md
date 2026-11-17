## Description:

Create interactive travel route maps from location names with real FlyAI hotel search and optional AI Vision-assisted extraction from travel planning images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rudy2steiner](https://clawhub.ai/user/rudy2steiner)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn ordered destination names, or POIs extracted from travel planning images by an image-capable agent, into editable interactive travel maps with route display and hotel search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local helper services may execute unsafe commands.

Mitigation: Review and replace shell execution with argument-array execution before installation or operation.

Risk: Local services may expose more workspace data than needed.

Mitigation: Bind services to loopback, restrict CORS and authentication where needed, and serve only a dedicated output directory.

Risk: Server management may stop unrelated processes that own expected ports.

Mitigation: Review port handling and avoid killing unknown port owners.

Risk: The release includes a shared Amap API key and unpinned dependencies.

Mitigation: Rotate or replace the shared key for deployment and pin dependencies during installation review.

Risk: Generated HTML and localStorage-rendered data may contain unsanitized content.

Mitigation: Sanitize generated HTML and localStorage-rendered values before using generated maps with untrusted inputs.

## Reference(s):

- [Travelmapify ClawHub release](https://clawhub.ai/rudy2steiner/skills/travelmapify)
- [rudy2steiner publisher profile](https://clawhub.ai/user/rudy2steiner)
- [Amap API Usage Guide](artifact/references/amap_api_guide.md)
- [POI Validation Rules](artifact/references/poi_validation_rules.md)
- [Travel Mapify Troubleshooting Guide](artifact/references/troubleshooting-guide.md)
- [amap-maps dependency](https://github.com/openclaw/openclaw/tree/main/skills/amap-maps)

## Skill Output:

**Output Type(s):** [files, shell commands, configuration, guidance]

**Output Format:** [HTML files plus concise command and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated maps are intended to be served over a local HTTP server and may use local helper services for geocoding and hotel search.]

## Skill Version(s):

2.2.2 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
