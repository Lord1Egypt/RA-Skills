## Description:

Generates images from text prompts by calling the Wavespeed AI NanoBanana2 API with configurable resolution and image format options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reroc8](https://clawhub.ai/user/reroc8)

### License/Terms of Use:


## Use Case:

Developers and agent users can use this skill to request image generation from text prompts through the Wavespeed AI service. It is intended for workflows that need generated visual assets and can provide a valid Wavespeed API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports unsafe automatic API execution and an exposed API key.

Mitigation: Review before installing; remove hard-coded credentials and any auto-running test block before use.

Risk: The security evidence reports a malformed manifest that can affect user-level skill configuration.

Mitigation: Replace the manifest with a valid skill manifest before registering or executing the skill.

Risk: The security evidence reports vulnerable dependencies.

Mitigation: Update dependencies and re-run security scanning before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/reroc8/skills/wavespeed-nanobanana2)
- [Wavespeed AI API Documentation](https://docs.wavespeed.ai/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON response with generated image API data or error details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WAVESPEED_API_KEY and a text prompt; optional resolution and output format parameters are documented by the artifact.]

## Skill Version(s):

1.0.3 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
