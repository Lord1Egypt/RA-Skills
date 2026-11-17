## Description:

This skill guides agents in using the WorkRally CLI to create media and manage projects, assets, canvases, and enterprise knowledge bases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to create images, video, audio, music, and 3D assets, and to manage WorkRally projects, shot lists, canvases, media libraries, and enterprise knowledge bases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation rules and automatic destination selection can send uploads to an unintended destination; uploaded images may be publicly readable.

Mitigation: Use the skill only for explicit WorkRally requests, identify the destination project and files, confirm unclear upload destinations, and treat uploaded images as publicly readable.

Risk: Destructive canvas changes and knowledge-base writes can affect shared or persistent content.

Mitigation: Require approval before destructive canvas changes or knowledge-base writes, and follow the documented stepwise destination confirmation.

Risk: The separately installed WorkRally CLI was not audited with the supplied documentation.

Mitigation: Review the installed CLI before relying on it for sensitive operations.

## Reference(s):

- [WorkRally](https://workrally.qq.com)
- [WorkRally API key setup](https://workrally.qq.com/open-api)
- [WorkRally on ClawHub](https://clawhub.ai/tencent-adm/skills/workrally)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration, Text, Images, Videos, Audio, 3D models]

**Output Format:** [CLI commands, text and structured results, and generated media assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the WorkRally CLI and the selected WorkRally project or canvas.]

## Skill Version(s):

2.12.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
