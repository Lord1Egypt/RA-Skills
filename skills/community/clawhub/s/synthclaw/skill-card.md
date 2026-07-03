## Description: <br>
Render Blender files with agent-controlled procedural parameters for synthetic data generation, including render quality metrics and dataset-wide diversity analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayakimovich](https://clawhub.ai/user/ayakimovich) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and ML/data engineers use SynthClaw to analyze Blender scenes, adjust procedural value nodes, and generate synthetic image datasets with accompanying render metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SynthClaw opens user-supplied .blend files in Blender while inheriting the caller environment, which can expose local secrets if a file is untrusted. <br>
Mitigation: Run it only on trusted .blend files or inside a sandbox/container with a scrubbed environment, limited filesystem access, and limited network access. <br>
Risk: Running Blender workflows in a session with cloud tokens, API keys, or other secrets in environment variables can expose those secrets to untrusted scene execution. <br>
Mitigation: Use a dedicated low-privilege execution environment and remove cloud tokens, API keys, and other sensitive environment variables before running the skill. <br>
Risk: The test blend creation script is not intended to run against an existing Blender project. <br>
Mitigation: Run test blend creation only in a disposable project directory or isolated test workspace. <br>


## Reference(s): <br>
- [SynthClaw Skill Page](https://clawhub.ai/ayakimovich/skills/synthclaw) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Analysis, Guidance] <br>
**Output Format:** [Rendered image files plus JSON status, metrics, and scene-analysis responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated images, compositor outputs, and dataset artifacts under caller-specified output paths.] <br>

## Skill Version(s): <br>
0.2.5 (source: frontmatter and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
