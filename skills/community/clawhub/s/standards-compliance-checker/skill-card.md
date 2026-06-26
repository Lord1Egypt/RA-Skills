## Description: <br>
Check data compliance with construction standards. Validate data against ISO 19650, IFC, COBie, UniFormat standards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, engineers, and construction project teams use this skill to validate project data against BIM and construction classification standards, review compliance issues, and generate structured summaries or exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Filesystem access can read or write project files explicitly provided to the agent. <br>
Mitigation: Install only if that access is acceptable, and review export paths before writing reports. <br>
Risk: Compliance results are advisory and validation coverage may have accuracy gaps, especially for OmniClass coverage. <br>
Mitigation: Review findings against authoritative standards before using them for compliance decisions. <br>


## Reference(s): <br>
- [Data Driven Construction](https://datadrivenconstruction.io) <br>
- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/standards-compliance-checker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Guidance] <br>
**Output Format:** [Structured Markdown tables and summaries, with optional CSV, Excel, or JSON exports when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided construction data and file paths; may write report exports when requested.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
