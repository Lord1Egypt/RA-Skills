## Description: <br>
Performs GeoJSON geometry analysis with SuperMap WebAssembly, including buffer, convex hull, intersection, union, erase, clip, distance, and topology operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nestone](https://clawhub.ai/user/nestone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and GIS practitioners use this skill to run local GeoJSON geometry operations from an agent workflow or command line, including spatial overlays, buffers, distance calculations, and file-based processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a bundled SuperMap WebAssembly component locally. <br>
Mitigation: Install only when the publisher is trusted and run with normal user privileges. <br>
Risk: Agent-supplied output paths can write geometry results to local files. <br>
Mitigation: Check output paths before allowing the agent to write results. <br>
Risk: Unexpected or unintended GeoJSON inputs can produce misleading spatial results. <br>
Mitigation: Provide only intended GeoJSON inputs and review generated geometry before using it in decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nestone/supermap-wasi-geo) <br>
- [NestOne publisher profile](https://clawhub.ai/user/nestone) <br>
- [SuperMap WASI Geometry usage guide](references/usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, files, shell commands, guidance] <br>
**Output Format:** [GeoJSON Feature objects or JSON result objects, optionally written to output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports inline GeoJSON input, file input, stdout output, pretty JSON formatting, and explicit output paths.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter and package.json list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
