## Description: <br>
Render restrained architecture diagrams from structured JSON with a deterministic local SVG renderer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leostehlik](https://clawhub.ai/user/leostehlik) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to turn structured node-and-edge JSON into clean SVG architecture diagrams for service maps, routing maps, and system relationship visuals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The renderer writes to the SVG output path supplied by the user and can create parent directories. <br>
Mitigation: Use intentional output paths, avoid pointing the renderer at files that should be preserved, and review generated SVGs before publishing or embedding them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leostehlik/visual-architecture) <br>
- [Publisher Profile](https://clawhub.ai/user/leostehlik) <br>
- [README](README.md) <br>
- [Example Service Map JSON](examples/service-map.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON examples and shell commands; the bundled renderer produces SVG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Input JSON describes diagram title, nodes, edges, optional labels, routing hints, and grid display.] <br>

## Skill Version(s): <br>
0.2.5 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
