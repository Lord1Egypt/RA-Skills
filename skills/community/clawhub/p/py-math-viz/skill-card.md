## Description:

Create clear math/data visualizations in Python and export to PNG using matplotlib, seaborn, and optional OpenCV post-processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rokokol](https://clawhub.ai/user/rokokol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to produce readable PNG charts for functions, datasets, simulations, trajectories, model comparisons, notes, and messaging workflows. It can render common plots from a JSON spec and tile generated images for comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled weather helper can send latitude, longitude, and timezone to Open-Meteo.

Mitigation: Require explicit user consent before using the weather helper with location data, or document and review that helper before deployment.

Risk: Large figure sizes, DPI values, or tiled image dimensions can consume significant local resources.

Mitigation: Review plot specs and bound figure size, DPI, and tile cell dimensions before running scripts on untrusted or oversized inputs.

## Reference(s):

- [Py Math Viz on ClawHub](https://clawhub.ai/rokokol/skills/py-math-viz)
- [Plot spec](references/spec.md)
- [Quick recipes](references/quick-recipes.md)
- [JSON spec recipes](references/recipes-spec-json.md)
- [Seaborn snippet recipes](references/recipes-seaborn-snippets.md)
- [Image tiling recipes](references/recipes-images.md)
- [Open-Meteo forecast endpoint](https://api.open-meteo.com/v1/forecast)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON specs, Python snippets, shell commands, and generated PNG file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces PNG visualization artifacts through local Python scripts; weather helper may call Open-Meteo when used.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
