## Description:

SynthClaw helps agents analyze Blender scenes, adjust procedural Value Nodes, render synthetic images or datasets, and return quality metrics such as Naturalness, LPIPS, and dataset diversity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayakimovich](https://clawhub.ai/user/ayakimovich)

### License/Terms of Use:

MIT

## Use Case:

Developers and ML data engineers use this skill to generate controlled synthetic image datasets from prepared Blender files, inspect scene parameters before rendering, and use image quality metrics to guide parameter tuning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run Blender locally on user-selected .blend files and inherits the process environment.

Mitigation: Use trusted .blend files, run the skill in a constrained environment where possible, and avoid exposing secrets through environment variables.

Risk: Dataset rendering can delete TIFF files under the selected output directory during cleanup.

Mitigation: Choose a fresh, dedicated output directory for each run so unrelated TIFF files cannot be removed.

Risk: Complex Blender scenes can be resource-intensive or time out during headless rendering.

Mitigation: Analyze the blend file first, start with EEVEE test renders, and set explicit timeouts or use production Cycles renders when appropriate.

## Reference(s):

- [ClawHub SynthClaw skill page](https://clawhub.ai/ayakimovich/skills/synthclaw)

## Skill Output:

**Output Type(s):** [files, text, configuration, guidance]

**Output Format:** [JSON status objects with rendered image or dataset file paths, logs, scene analysis, and optional metric values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce PNG render outputs, routed compositor outputs, dataset directories, and Naturalness, LPIPS, or Shannon entropy metrics when dependencies and inputs are available.]

## Skill Version(s):

0.2.6 (source: frontmatter and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
