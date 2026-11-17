## Description:

Comprehensive Three.js 3D graphics reference for building 3D web apps, games, and visualizations with scene setup, cameras, geometries, materials, lights, shadows, post-processing, controls, animation, loaders, textures, TSL/node materials, math utilities, and debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as a practical Three.js reference when building or reviewing 3D browser experiences, games, visualizations, and rendering workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Three.js examples may load models, textures, or decoder files from external URLs.

Mitigation: Review generated app code before running it, prefer trusted or pinned asset locations, and verify external resources used by loaders.

Risk: 3D rendering examples can create performance or memory pressure when assets, render targets, textures, or animation loops are not bounded.

Mitigation: Cap pixel ratio and texture sizes, dispose Three.js resources after use, and test generated scenes on target browsers and devices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlark/skills/threejs-3d)
- [Getting Started - Advanced Patterns](references/getting-started.md)
- [Cameras](references/cameras.md)
- [Geometries](references/geometries.md)
- [Materials](references/materials.md)
- [Lights & Environments](references/lights.md)
- [Objects & Scene Graph](references/objects.md)
- [Textures](references/textures.md)
- [Loaders](references/loaders.md)
- [Animation](references/animation.md)
- [Controls & Labels](references/controls.md)
- [Math Utilities](references/math.md)
- [Renderers, Post-Processing & Shadows](references/renderers.md)
- [Node Materials & TSL](references/nodes.md)
- [Helpers & Debugging](references/helpers.md)
- [Example Draco decoder URL](https://www.gstatic.com/draco/versioned/decoders/1.5.7/)
- [Example KTX2 transcoder URL](https://unpkg.com/three@0.170.0/examples/jsm/libs/basis/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reference-oriented output; generated app code should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
