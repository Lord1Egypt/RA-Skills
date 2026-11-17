## Description:

Generate UGC-style promotional videos with AI lip-sync from an image of a person with a product and a pure-dialogue script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pauldelavallaz](https://clawhub.ai/user/pauldelavallaz)

### License/Terms of Use:


## Use Case:

External creators, marketers, and developers use this skill to turn approved product-person images and dialogue scripts into AI-generated promotional videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local image files and send scripts to ComfyDeploy and downstream media services.

Mitigation: Use only non-sensitive images and scripts that are approved for those services, and run with a narrowly scoped ComfyDeploy API key.

Risk: The security summary flags local file upload and output download paths as too broadly scoped for a media-generation tool.

Mitigation: Avoid arbitrary local paths, run in a restricted workspace, and review the intended input and output paths before execution.

Risk: The security guidance recommends review before installing and dependency pinning before use.

Mitigation: Review the skill before installation, scan it before deployment, and pin dependencies for controlled environments.

## Reference(s):

- [ClawHub VEED UGC Skill Page](https://clawhub.ai/pauldelavallaz/skills/veed-ugc)
- [ComfyDeploy Deployment Queue Endpoint](https://api.comfydeploy.com/api/run/deployment/queue)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [MP4 video file with command-line status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.10 or newer, httpx, a ComfyDeploy API key, an image URL or local image file, pure-dialogue script text, and an optional ElevenLabs voice ID.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
