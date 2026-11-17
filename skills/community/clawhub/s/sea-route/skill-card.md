## Description:

Generates approximate maritime routes between two ports or coordinate pairs, including route waypoints, estimated distance and travel time, and an interactive HTML map.

This skill is ready for commercial/non-commercial use.

## Publisher:

[f2quantum](https://clawhub.ai/user/f2quantum)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and logistics-focused agents use this skill to answer maritime route, shipping lane, port distance, travel time, and waypoint requests for visualization and planning support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can include unescaped route labels.

Mitigation: Use trusted origin and destination names, avoid labels supplied by untrusted users, and HTML-escape labels before opening or sharing generated maps.

Risk: Dependencies are fetched at runtime and are not pinned to exact versions.

Mitigation: Run in a controlled environment and pin or review searoute and folium versions before operational use.

Risk: Routes are approximate and not suitable for real vessel navigation.

Mitigation: Use outputs for visualization and planning support only, and verify any operational route with authoritative maritime navigation tools.

## Reference(s):

- [Sea Route Navigation release page](https://clawhub.ai/f2quantum/skills/sea-route)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, files, guidance]

**Output Format:** [Markdown response with route summary and waypoint table, JSON stdout from the script, and an HTML map file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python >=3.9, uv, and runtime installation of searoute and folium dependencies; generated routes are approximate and not intended for real navigation.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
