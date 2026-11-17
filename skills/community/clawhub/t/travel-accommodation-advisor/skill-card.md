## Description:

Finds and compares bookable hotels near a specified city landmark by anchoring on a POI, filtering by radius, and sorting by distance or quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill when a city landmark is known and they need a short list of comparable, bookable hotels near that landmark.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned global npm CLI.

Mitigation: Prefer a pinned local FlyAI CLI installation in a constrained environment and avoid elevated privileges for npm install.

Risk: An optional FlyAI API key may persist in local FlyAI configuration.

Mitigation: Review where flyai stores configuration before adding an API key and keep credentials out of shared logs or generated recommendations.

Risk: Hotel recommendations depend on live FlyAI and Fliggy data and can be incomplete when POI or hotel searches return no results.

Mitigation: Use the documented fallback flow to relax keywords, budget, star rating, or radius constraints, and clearly label approximate POI or radius matches.

## Reference(s):

- [FlyAI homepage](https://open.fly.ai/)
- [Playbooks](references/playbooks.md)
- [Templates](references/templates.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown with hotel comparison tables, image rows, booking links, and optional CLI command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires city, landmark, check-in date, and check-out date; optional radius, budget, hotel stars, and sorting preference.]

## Skill Version(s):

1.0.0 (source: artifact metadata and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
