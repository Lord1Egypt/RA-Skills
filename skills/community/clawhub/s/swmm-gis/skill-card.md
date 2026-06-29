## Description: <br>
GIS/DEM preprocessing for SWMM experiments using the user's own QGIS/GRASS layers, including subcatchment delineation, QGIS-derived polygon preprocessing, entropy hotspot ranking, and reproducible workflow guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhonghao1995](https://clawhub.ai/user/zhonghao1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare watershed GIS and DEM inputs for SWMM workflows, generate subcatchment and parameter handoff files, and inspect entropy-guided spatial heterogeneity before model building. The workflow is intended for local processing of user-supplied QGIS/GRASS layers and does not by itself validate calibrated hydrologic performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local GIS processing scripts read user-supplied watershed files and write SWMM/QGIS outputs, including behavior that can overwrite files in run or final_layers directories. <br>
Mitigation: Use a fresh dedicated run/final_layers directory, keep backups of original GIS data, and inspect generated manifests before relying on outputs. <br>
Risk: The workflow depends on external Agentic SWMM, QGIS, GRASS, and SWMM tooling that is outside the skill package. <br>
Mitigation: Review and complete the separate installation steps for those dependencies before executing generated commands. <br>


## Reference(s): <br>
- [ClawHub Swmm Gis release page](https://clawhub.ai/zhonghao1995/swmm-gis) <br>
- [Agentic SWMM workflow](https://github.com/Zhonghao1995/agentic-swmm-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and file path lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When the referenced scripts run, they can write CSV, JSON, GeoJSON, shapefile, raster, PNG, manifest, and audit outputs under user-selected run directories.] <br>

## Skill Version(s): <br>
0.7.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
