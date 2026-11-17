## Description:

Seedance 2.0 Pro on RunComfy helps agents generate short cinematic video clips with multi-modal references, native lip-sync audio, camera-motion prompts, and the RunComfy CLI endpoint `bytedance/seedance-v2/pro`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and agent operators use this skill to route Seedance video-generation requests through RunComfy, including text-to-video, image/video/audio-referenced clips, short ad concepts, lip-synced spokesperson clips, and cinematic previs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the external RunComfy CLI globally can introduce supply-chain exposure.

Mitigation: Use a pinned or project-local @runcomfy/cli version and avoid sudo for npm installs.

Risk: RUNCOMFY_TOKEN grants access to RunComfy services if exposed.

Mitigation: Keep RUNCOMFY_TOKEN out of shell startup files and use scoped secret management for CI or containers.

Risk: Prompts and media URLs are sent to RunComfy for generation.

Mitigation: Only submit prompts and image, video, or audio URLs that are appropriate to share with RunComfy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/permew/skills/seedance-v2)
- [RunComfy website](https://www.runcomfy.com)
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=seedance-v2)
- [Seedance 2.0 Pro model page](https://www.runcomfy.com/models/bytedance/seedance-v2/pro?utm_source=clawhub&utm_medium=skill&utm_campaign=seedance-v2)
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=seedance-v2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media is produced by RunComfy outside the skill response and downloaded to the requested output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
