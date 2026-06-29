## Description: <br>
Build, validate, and route SWMM pipe-network models for urban drainage from raw municipal shapefiles or structured GIS/CAD exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhonghao1995](https://clawhub.ai/user/zhonghao1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and drainage-modeling engineers use this skill to convert municipal storm-pipe, GIS, or structured asset-export data into SWMM-ready network JSON, QA the topology and hydraulic attributes, route subcatchments to network nodes, and export network sections for INP assembly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a separate Agentic SWMM toolchain and MCP servers for execution. <br>
Mitigation: Review the external Agentic SWMM project and installation requirements before installing or running that separate toolchain. <br>
Risk: The skill reads municipal drainage and GIS/model files selected by the user and writes derived model files to supplied output paths. <br>
Mitigation: Use trusted input datasets, confirm output paths before execution, and review generated network files before using them in downstream modeling. <br>
Risk: Default or inferred drainage attributes such as invert elevations, outfall selection, or pipe orientation can produce misleading model behavior if left unreviewed. <br>
Mitigation: Run the provided QA step, inspect warnings, and replace defaults with measured or otherwise justified engineering data before relying on model results. <br>


## Reference(s): <br>
- [Agentic SWMM project](https://github.com/Zhonghao1995/agentic-swmm-workflow) <br>
- [Mapping templates for import_city_network](artifact/templates/README.md) <br>
- [City dual-system structured network benchmark](artifact/examples/city-dual-system/README.md) <br>
- [ClawHub skill page](https://clawhub.ai/zhonghao1995/swmm-network) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration, file paths, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or guides creation of SWMM network JSON, routed subcatchment CSV files, QA reports, and SWMM INP network sections through the referenced toolchain.] <br>

## Skill Version(s): <br>
0.7.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
