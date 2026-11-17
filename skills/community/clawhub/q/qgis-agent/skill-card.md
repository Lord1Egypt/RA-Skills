## Description:

QGIS Agent lets AI agents drive local QGIS Processing algorithms over HTTP for vector, raster, terrain, interpolation, network, format conversion, and map rendering workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaojj662](https://clawhub.ai/user/zhaojj662)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, GIS analysts, and agent builders use this skill to let an AI agent discover QGIS algorithms, inspect their parameters, run spatial analysis chains, manage QGIS projects, and render map outputs through a local service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill opens an unauthenticated local QGIS control service that can read and write files.

Mitigation: Use it only for trusted local workflows, keep it bound to localhost, run it under a low-privilege account, and set QGIS_ALLOWED_PATHS to dedicated input and output folders.

Risk: The server can create or overwrite GIS project, data, and render outputs.

Mitigation: Confirm output paths before write or render operations and keep analysis outputs in a dedicated workspace.

Risk: Optional PyQGIS execution can run arbitrary Python code when enabled.

Mitigation: Leave PYQGIS_ENABLE_EXEC disabled unless running in an isolated trusted environment where arbitrary Python execution is acceptable.

## Reference(s):

- [QGIS Agent API](configs/api.md)
- [QGIS Agent Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/zhaojj662/skills/qgis-agent)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Files, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with curl examples, JSON request and response bodies, and generated GIS output file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include GeoPackage, raster, project, and PNG render files produced by local QGIS processing.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
