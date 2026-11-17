## Description:

Upscale and enhance media with Topaz through RunAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to submit image or video enhancement tasks to Topaz through RunAPI, then verify and retrieve the requested media outputs. It supports one-off CLI execution and SDK-oriented integration planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the RunAPI CLI through the Homebrew tap introduces dependency-trust risk.

Mitigation: Confirm trust in the RunAPI Homebrew tap and prefer a reviewed or pinned CLI version when available.

Risk: Using the skill can upload local media to RunAPI for Topaz processing.

Mitigation: Only submit media files that are appropriate to upload to RunAPI, and provide only a RunAPI API key intended for this tool.

## Reference(s):

- [RunAPI Topaz model page](https://runapi.ai/models/topaz)
- [Topaz model overview, pricing, and rate limits](https://runapi.ai/models/topaz.md)
- [Topaz provider overview](https://runapi.ai/providers/topaz.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [RunAPI Topaz SDK](https://github.com/runapi-ai/topaz-sdk)
- [Topaz image upscale operation](https://runapi.ai/models/topaz/upscale-image.md)
- [Topaz video upscale operation](https://runapi.ai/models/topaz/upscale-video.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown with inline shell commands, JSON request and response files, and saved media deliverables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the RunAPI CLI for one-off execution and may use RUNAPI_API_KEY or saved CLI authentication.]

## Skill Version(s):

0.2.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
