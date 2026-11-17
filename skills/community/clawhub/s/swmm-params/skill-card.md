## Description:

Deterministic mapping from land use and soil texture to SWMM runoff/subarea and Green-Ampt infiltration parameters for first-pass subcatchment parameter tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhonghao1995](https://clawhub.ai/user/zhonghao1995)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate auditable JSON parameter tables from land-use and soil CSV inputs for SWMM-oriented modeling workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback lookup rows may mask missing land-use or soil classes in production modeling.

Mitigation: Use --strict for auditable runs and review unmatched-key lists and count summaries before relying on generated defaults.

Risk: The documented MCP wrapper is referenced but not included in the artifact.

Mitigation: Confirm local paths and wrapper availability before using MCP commands; use the bundled Python scripts directly when the wrapper is absent.

Risk: Generated defaults are first-pass model parameters and may not reflect calibrated local hydrology.

Mitigation: Review and calibrate generated SWMM parameters before production modeling.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhonghao1995/skills/swmm-params)
- [Agentic SWMM Project](https://github.com/Zhonghao1995/agentic-swmm-workflow)
- [Land Use Lookup Table](references/landuse_class_to_subcatch_params.csv)
- [Soil Texture Green-Ampt Lookup Table](references/soil_texture_to_greenampt.csv)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python command examples and JSON output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deterministic CSV-to-JSON mapping guidance and describes generated records, SWMM-oriented sections, unmatched-key lists, and count summaries.]

## Skill Version(s):

0.7.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
