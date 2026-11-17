## Description:

Author, load, and troubleshoot Reality Composer Pro Shader Graph materials for RealityKit on visionOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomkrikorian](https://clawhub.ai/user/tomkrikorian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to author RealityKit Shader Graph materials, load them with ShaderGraphMaterial, expose promoted inputs for runtime control, and troubleshoot exported USD or MaterialX only when debugging or interoperability requires it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Shader Graph, USD, or MaterialX changes may alter project material assets or produce incorrect rendering.

Mitigation: Review proposed asset changes in source control and validate them in Reality Composer Pro or the target RealityKit app before release.

Risk: The skill references sample Shader Graph assets that are not included in this package.

Mitigation: Confirm any referenced sample file exists in the local project before using it, or adapt the guidance manually.

Risk: Undocumented exported USD or MaterialX details may not remain stable across Apple tooling versions.

Mitigation: Prefer Reality Composer Pro authoring and promoted inputs for runtime control; inspect exported USD or MaterialX only for debugging, interoperability, or asset review.

## Reference(s):

- [ShaderGraph Nodes for Apple RealityKit](references/REFERENCE.MD)
- [Apple Shader Graph documentation](https://developer.apple.com/documentation/shadergraph/)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with inline code and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Shader Graph, USD, or MaterialX asset changes for human review; no executable payloads are included.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
