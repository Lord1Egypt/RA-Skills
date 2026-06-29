## Description: <br>
Render Blender files with agent-controlled procedural parameters for synthetic data generation, including Naturalness, LPIPS, and dataset diversity metrics that help agents iteratively tune parameter ranges for more useful synthetic data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayakimovich](https://clawhub.ai/user/ayakimovich) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and ML or data engineers use SynthClaw to analyze Blender scenes, adjust named procedural Value Nodes, render CYCLES or EEVEE images and datasets, and use returned quality metrics to iterate on synthetic training data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Blender jobs on user-selected .blend files. <br>
Mitigation: Review third-party .blend files before use and run Blender in a sandboxed or otherwise constrained process when files are untrusted. <br>
Risk: The skill can write generated renders and remove cleanup targets inside caller-selected output folders. <br>
Mitigation: Use a dedicated empty output directory for each run and avoid broad paths such as a home directory, project root, or shared workspace. <br>
Risk: Rendering and metric computation may read local scene and image files while sensitive environment variables are present. <br>
Mitigation: Run with only the environment variables needed for Blender execution and avoid processing sensitive reference images unless required. <br>


## Reference(s): <br>
- [SynthClaw ClawHub listing](https://clawhub.ai/ayakimovich/skills/synthclaw) <br>
- [Skill definition](SKILL.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Analysis, Guidance] <br>
**Output Format:** [JSON status objects with local render or dataset file paths, logs, scene analysis, and optional Naturalness, LPIPS, or diversity metrics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Blender 4.0+ in PATH; CYCLES is used for production rendering and EEVEE for faster tests.] <br>

## Skill Version(s): <br>
0.2.3 (source: SKILL.md frontmatter, pyproject.toml, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
