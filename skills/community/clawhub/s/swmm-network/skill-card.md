## Description:

Builds, validates, and routes SWMM pipe-network models for urban drainage from municipal shapefiles or structured GIS/CAD exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhonghao1995](https://clawhub.ai/user/zhonghao1995)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare SWMM-ready network JSON, QA drainage topology and attributes, attach subcatchments to upstream nodes, and export core SWMM INP sections from real pipe-network data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted GIS text can be written into SWMM input files without escaping or validation.

Mitigation: Validate node IDs, link IDs, and textual fields before INP export; reject newlines, brackets, and comment delimiters; inspect generated INP files before running simulations.

Risk: Raw municipal pipe layers may contain missing elevation, orientation, or connectivity data that can produce misleading hydraulic models.

Mitigation: Run the documented outfall inference, endpoint snapping, pipe reorientation, and QA steps, then review warnings such as missing inverts or missing paths to an outfall before handing results to downstream builders.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhonghao1995/skills/swmm-network)
- [Agentic SWMM project](https://github.com/Zhonghao1995/agentic-swmm-workflow)
- [Mapping templates README](templates/README.md)
- [SWMM network model schema](scripts/schema/network_model.schema.json)
- [City dual-system example](examples/city-dual-system/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, CSV, GeoJSON, and SWMM INP file outputs from the supporting tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces single-stream agent guidance and may direct execution of local Python tools that create or validate network.json, mapping.json, routed subcatchment CSV, GeoJSON, QA JSON, and INP text outputs.]

## Skill Version(s):

0.7.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
