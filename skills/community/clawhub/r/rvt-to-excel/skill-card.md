## Description:

Convert RVT/RFA files to Excel databases. Extract BIM element data, properties, and quantities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Developers, BIM engineers, and construction data teams use this skill to convert Revit RVT/RFA files into structured Excel data for quantity takeoffs, reporting, and downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to run a third-party RvtExporter executable without a pinned version or built-in verification evidence.

Mitigation: Use a specific reviewed release, verify its hash or code signature when available, install it at an explicit trusted path, and run it only after confirming the source is trusted.

Risk: The workflow requires filesystem access to Revit project files and Excel output folders.

Mitigation: Run conversion with access limited to the required input and output directories, especially when batch processing project folders.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/skills/rvt-to-excel)
- [cad2data Pipeline](https://github.com/datadrivenconstruction/cad2data-Revit-IFC-DWG-DGN-pipeline-with-conversion-validation-qto)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe or produce Excel conversion workflows that invoke a locally installed DDC RvtExporter executable.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact/claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
