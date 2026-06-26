## Description: <br>
Upscale and enhance media with Topaz through RunAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to upscale or enhance images and videos with Topaz through RunAPI. It supports one-off CLI tasks and points developers to SDKs for application integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images, videos, and request metadata are sent to an external RunAPI/Topaz service for processing. <br>
Mitigation: Use the skill only for media appropriate for external processing, and review the service privacy, retention, and authentication terms before using sensitive private media. <br>
Risk: The skill relies on the RunAPI CLI and optional API-key authentication. <br>
Mitigation: Install the RunAPI CLI from the declared Homebrew tap, authenticate with runapi login or RUNAPI_API_KEY, and keep credentials out of generated files and shared logs. <br>


## Reference(s): <br>
- [RunAPI Topaz homepage](https://runapi.ai/models/topaz) <br>
- [Topaz model overview, pricing, and rate limits](https://runapi.ai/models/topaz.md) <br>
- [Topaz provider comparison](https://runapi.ai/providers/topaz.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>
- [Topaz image upscale](https://runapi.ai/models/topaz/image-upscale.md) <br>
- [Topaz video upscale](https://runapi.ai/models/topaz/video-upscale.md) <br>
- [ClawHub skill page](https://clawhub.ai/runapi-ai/runapi-topaz) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and package names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents toward RunAPI CLI usage for one-off tasks and SDK usage for application integration.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
