## Description:

Create interactive travel route maps from location names with real FlyAI hotel search. Supports AI Vision analysis of travel planning images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rudy2steiner](https://clawhub.ai/user/rudy2steiner)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn ordered travel locations or AI-vision-extracted points of interest into shareable interactive HTML route maps with geocoding, editing, and hotel search support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local services started by the skill may expose workspace files or remain running after use.

Mitigation: Run the skill only in a dedicated workspace without private files, bind services to local-only interfaces, avoid shared networks, and stop all background servers after use.

Risk: Security evidence reports command-injection risk and possible termination of unrelated processes.

Mitigation: Review and fix the package before normal installation, restrict inputs and execution privileges, and avoid running it in a privileged or multi-project environment.

Risk: The skill depends on Amap and FlyAI integrations, including an unpinned global FlyAI installation path.

Mitigation: Use a restricted Amap key, pin and verify FlyAI installation where possible, and validate external service behavior before relying on generated maps.

## Reference(s):

- [Travel Mapify on ClawHub](https://clawhub.ai/rudy2steiner/skills/travel-mapify)
- [Amap Maps Required Skill](https://github.com/openclaw/openclaw/tree/main/skills/amap-maps)
- [Amap API Usage Guide](references/amap_api_guide.md)
- [POI Validation Rules](references/poi_validation_rules.md)
- [Troubleshooting Guide](references/troubleshooting-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces self-contained interactive HTML maps intended to be served over a local HTTP server.]

## Skill Version(s):

2.2.2 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
