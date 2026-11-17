## Description:

Generate talking head videos from a photo using VEED Fabric 1.0. Triggers on mentions of "veed", "fabric", or "talking video". Turns a headshot + audio or text script into a lip-synced MP4 video via fal.ai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mattdotroberts](https://clawhub.ai/user/mattdotroberts)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, founders, and developers use this skill to turn a supplied face photo plus audio or a text script into a lip-synced MP4 talking-head video through VEED Fabric and fal.ai.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected photos, audio, scripts, and generated videos may be sent to fal.ai/VEED infrastructure and local media may become reachable through CDN URLs.

Mitigation: Use only media with appropriate consent, avoid sensitive face or voice data, and install from a pinned or reviewed release.

Risk: The skill uses a fal.ai API key for queue submission, polling, upload, and retrieval workflows.

Mitigation: Use a limited-scope fal.ai key where possible and keep the key in the FAL_KEY environment variable rather than sharing it inline.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mattdotroberts/skills/veed-skill)
- [VEED Fabric 1.0 model](https://fal.ai/models/veed/fabric-1.0)
- [fal.ai API key dashboard](https://fal.ai/dashboard/keys)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash and JSON examples; generated video is saved as an MP4 file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads completed videos to ./output/ and reports the local path, hosted fal.ai URL, and file size when available.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
