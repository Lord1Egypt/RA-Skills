## Description: <br>
Render Blender files with agent-controlled procedural parameters for synthetic data generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayakimovich](https://clawhub.ai/user/ayakimovich) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and ML data engineers use SynthClaw to inspect Blender scenes, adjust named procedural Value Nodes, render individual images or datasets, and return quality and diversity metrics for synthetic data workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided .blend files can cause Blender jobs to access local files, environment data, or processes outside the intended rendering task. <br>
Mitigation: Run only trusted .blend files, or execute the skill inside a sandboxed or containerized environment with no API keys, cloud credentials, session tokens, or sensitive local paths. <br>
Risk: Long CYCLES renders or large dataset jobs can consume substantial CPU, GPU, memory, or disk resources. <br>
Mitigation: Start with EEVEE or small sample counts, keep render timeouts enabled, and apply host-level resource limits for shared or production systems. <br>
Risk: Naturalness, LPIPS, and entropy metrics are heuristic signals and may not prove that generated data is fit for a specific downstream model or domain. <br>
Mitigation: Validate generated outputs against task-specific acceptance criteria and review representative samples before using the dataset for training or evaluation. <br>


## Reference(s): <br>
- [SynthClaw Skill Definition](SKILL.md) <br>
- [SynthClaw README](README.md) <br>
- [ClawHub SynthClaw Skill Page](https://clawhub.ai/ayakimovich/skills/synthclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Analysis] <br>
**Output Format:** [Rendered image or dataset files with JSON status, output paths, Blender scene analysis, and quality or diversity metrics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Blender 4.0+ or 5.0+ in PATH; supports EEVEE for fast testing and CYCLES for production rendering.] <br>

## Skill Version(s): <br>
0.2.1 (source: frontmatter, pyproject.toml, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
