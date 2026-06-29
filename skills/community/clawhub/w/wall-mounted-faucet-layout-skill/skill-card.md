## Description: <br>
Calculate, validate, and visualize wall-mounted faucet installation geometry, especially faucet reach L and outlet height H1 for product selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[starsy](https://clawhub.ai/user/starsy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, installers, and other external users use this skill to calculate wall-mounted faucet reach, outlet height, drain position, stream angle, and related basin geometry, then validate the result before installation. When a visual handoff is useful, the skill can produce an annotated SVG diagram for the same geometry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated faucet geometry may be treated as final installation guidance even though it is a straight-line estimate. <br>
Mitigation: Confirm dimensions and water behavior with an on-site mock-up or water-flow test before concealed installation work. <br>
Risk: The skill can run local Python scripts and write SVG diagrams to disk. <br>
Mitigation: Use a deliberate project output path for generated diagrams and inspect SVG output before sharing it or using it for installation handoff. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/starsy/wall-mounted-faucet-layout-skill) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Geometry diagram](artifact/assets/wall_mounted_faucet_geometry_v2.svg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, files, guidance] <br>
**Output Format:** [Markdown guidance with formulas, numeric results, validation notes, command examples, and optional SVG file output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calculations use supplied dimensions and a straight-line water path model; optional diagram generation writes an SVG file to a user-selected path.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
