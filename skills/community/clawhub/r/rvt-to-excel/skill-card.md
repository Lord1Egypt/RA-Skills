## Description: <br>
Convert RVT/RFA files to Excel databases. Extract BIM element data, properties, and quantities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, BIM engineers, and construction analysts use this skill to plan and run local RVT/RFA exports into Excel workbooks for quantity takeoffs, model data review, and downstream analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on a separate local RvtExporter.exe, so an untrusted exporter binary could affect local files or exported results. <br>
Mitigation: Install and run only a trusted exporter binary, and execute conversions on specific intended RVT/RFA files or folders. <br>
Risk: Batch conversions and generated Excel files may overwrite existing outputs or expose detailed building model data and quantities. <br>
Mitigation: Check for existing matching .xlsx files before batch jobs and protect generated spreadsheets according to the project's data handling requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/rvt-to-excel) <br>
- [cad2data Revit/IFC/DWG/DGN pipeline](https://github.com/datadrivenconstruction/cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local filesystem access and a separately trusted RvtExporter.exe; generated spreadsheets may contain detailed building model data.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
