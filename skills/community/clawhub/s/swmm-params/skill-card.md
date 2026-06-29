## Description: <br>
Deterministic mapping from land use and soil texture to SWMM runoff/subarea and Green-Ampt infiltration parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhonghao1995](https://clawhub.ai/user/zhonghao1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers can use this skill to generate first-pass SWMM subcatchment parameter tables from land use and soil CSV inputs. It supports auditable CSV-to-JSON mapping before downstream SWMM builder workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SWMM parameters may be incorrect for engineering decisions if treated as calibrated model inputs. <br>
Mitigation: Review and calibrate generated parameters before using them for engineering analysis or decisions. <br>
Risk: Fallback lookup rows can mask unmapped land use classes or soil textures. <br>
Mitigation: Use the scripts' strict mode for production-style runs and review unmatched-key summaries in the JSON output. <br>
Risk: The scripts write JSON to user-provided output paths. <br>
Mitigation: Choose output paths deliberately and review generated files before passing them into downstream SWMM tooling. <br>


## Reference(s): <br>
- [Land use lookup table](references/landuse_class_to_subcatch_params.csv) <br>
- [Soil texture lookup table](references/soil_texture_to_greenampt.csv) <br>
- [Agentic SWMM workflow](https://github.com/Zhonghao1995/agentic-swmm-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON file outputs from the bundled scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated JSON includes records, SWMM-oriented sections, unmatched or incomplete ID summaries, and counts.] <br>

## Skill Version(s): <br>
0.7.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
