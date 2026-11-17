## Description:

Calls the Tukeli visual processing API for background removal, face enhancement, and AI background replacement using uploaded image files or image URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cutout-pro](https://clawhub.ai/user/cutout-pro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to route image-processing tasks to Tukeli, including matting, clearer face images, and AI-generated replacement backgrounds. It is useful when an agent needs CLI-driven image API calls with setup and API reference guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends selected images, image URLs, prompts, optional facial landmark data, and an API key to Tukeli's external paid service.

Mitigation: Use a scoped API key in an isolated environment, avoid sensitive image inputs unless approved, and confirm the provider's data handling terms before use.

Risk: The security review warns that documented local usage limits may not be implemented or provider-enforced.

Mitigation: Rely on provider-side quota and billing controls, monitor credit usage, and do not treat local daily-limit settings as a hard safeguard.

Risk: Dependency pinning should be reviewed before deployment.

Mitigation: Review and pin Python dependencies in the deployment environment before installing or running the skill.

## Reference(s):

- [Setup Guide](references/setup-guide.md)
- [API Reference](references/api-reference.md)
- [Tukeli API base endpoint](https://picupapi.tukeli.net)
- [Tukeli website](https://www.tukeli.net)
- [Tukeli image matting API documentation](https://www.tukeli.net/apidoc-image-matting.html)
- [ClawHub skill page](https://clawhub.ai/cutout-pro/skills/tukeli-visual-api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Files]

**Output Format:** [Markdown guidance with CLI commands; API responses may be PNG files, Base64 JSON, or task status JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TUKELI_API_KEY. Processed image files and metadata are written under data/outputs when the bundled script is used.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, scripts/tukeli.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
