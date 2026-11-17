## Description:

Converts input images or prompt to 3D models using Hyper3D Rodin Gen-2 API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whitegiven](https://clawhub.ai/user/whitegiven)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical creators use this skill to generate 3D model assets from images or text prompts through the Hyper3D Rodin Gen-2 API. It helps configure requests, poll task status, and retrieve generated assets in formats such as GLB, USDZ, FBX, OBJ, and STL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling needs review before installation.

Mitigation: Use a dedicated Hyper3D API key with limited billing exposure, prefer environment-based secret handling, and avoid passing keys with --api-key or printing them.

Risk: Images and prompts submitted through the skill are sent to Hyper3D.

Mitigation: Avoid submitting sensitive inputs unless sharing them with Hyper3D is acceptable for the intended use case.

Risk: Remote-controlled downloads and local output paths need caution before use in sensitive directories.

Mitigation: Run downloads in a disposable output directory and review filename and URL handling before using the script in project or home directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whitegiven/skills/rodin3d-skill)
- [Hyper3D API dashboard](https://hyper3d.ai/api-dashboard)
- [Hyper3D Rodin generation endpoint](https://api.hyper3d.com/api/v2/rodin)
- [Hyper3D task status endpoint](https://api.hyper3d.com/api/v2/status)
- [Hyper3D result download endpoint](https://api.hyper3d.com/api/v2/download)
- [Example asset guidance](artifact/assets/examples/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with Python and shell command examples; generated model downloads are written as local files when an output directory is provided.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports image or prompt inputs, configurable Rodin tiers, GLB/USDZ/FBX/OBJ/STL output formats, polling, and temporary download links.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
