## Description: <br>
Sea route navigation: generate the shortest maritime route between two ports or coordinates, output navigation waypoints and an interactive HTML map. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[f2quantum](https://clawhub.ai/user/f2quantum) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to estimate maritime routes between ports or coordinates, including distance, travel time, waypoints, and a local interactive map for route visualization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route outputs are approximate and intended for visualization or estimation rather than real vessel navigation. <br>
Mitigation: Use the generated route only for planning discussion or visualization, and rely on authoritative nautical charts and navigation systems for operational decisions. <br>
Risk: Generated HTML map files and route labels may expose route details or names if saved in sensitive locations or shared. <br>
Mitigation: Save maps to non-sensitive paths, avoid untrusted route labels, and review generated files before sharing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/f2quantum/sea-route) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, HTML files, shell commands, guidance] <br>
**Output Format:** [JSON route data with a Markdown-facing summary and a generated HTML map file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes origin and destination coordinates, distance, estimated duration, waypoint coordinates, and the saved map path.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
