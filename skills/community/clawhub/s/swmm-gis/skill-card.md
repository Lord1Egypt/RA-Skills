## Description:

GIS/DEM preprocessing for SWMM experiments using the user's own QGIS/GRASS layers, including subcatchment delineation, preprocessing, entropy hotspot analysis, and QGIS/GRASS-backed reproducible workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhonghao1995](https://clawhub.ai/user/zhonghao1995)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare local GIS/DEM inputs for SWMM experiments, including QGIS/GRASS watershed processing, subcatchment metrics, entropy-guided partitioning, and builder-ready CSV/JSON handoffs. It is intended for user-provided project data and does not by itself establish calibrated hydrologic performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local QGIS/GRASS/Python preprocessing over user-provided DEM and vector data.

Mitigation: Run it only on project data you trust and in an isolated working directory with expected GIS dependencies installed.

Risk: Final-layer packaging can overwrite files named subcatchments, flow, outfall, slope_percent.tif, overview.png, and manifest.json in the selected output directory.

Mitigation: Use a dedicated run or output directory for each case and keep separate backups of existing deliverables.

Risk: CRS normalization can reproject, clip, or resample layers, which may change watershed structure.

Mitigation: Validate CRS and raster alignment first, and normalize only when the input layers actually need harmonization.

Risk: The workflow produces GIS-derived SWMM subcatchment units and audit evidence but does not prove calibrated hydrologic performance.

Mitigation: Pass outputs through the downstream SWMM builder, runner, and experiment audit workflow before relying on hydrologic conclusions.

Risk: The skill documentation depends on the external Agentic SWMM project for the executable toolchain and MCP server.

Mitigation: Review the external project and its installation requirements before relying on that toolchain.

## Reference(s):

- [ClawHub Swmm Gis Skill Page](https://clawhub.ai/zhonghao1995/skills/swmm-gis)
- [Agentic SWMM Project Link From Skill Documentation](https://github.com/Zhonghao1995/agentic-swmm-workflow)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands and local file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local GIS/SWMM artifacts such as CSV, JSON, shapefiles, rasters, PNG overview figures, manifests, and audit files when the referenced tools are run.]

## Skill Version(s):

0.7.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
