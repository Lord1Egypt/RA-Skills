## Description:

Provides fallback vision/image understanding for agents when the primary model cannot interpret an image, calling an OpenAI-compatible vision API and returning structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vst93](https://clawhub.ai/user/vst93)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill when a primary model lacks image support or returns insufficient image understanding, especially for UI screenshots, terminal output, mobile app screens, and layout reconstruction. It turns an image plus optional OCR or failure context into a structured vision result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image contents, OCR text, and prior model output may be sent to the configured vision provider.

Mitigation: Use the skill only with data appropriate for the selected provider, and configure trusted HTTPS-only endpoints.

Risk: API credentials and provider settings may be read from environment variables or dotenv-style files.

Mitigation: Prefer explicit VISION_API_KEY or a user-owned env file, avoid /root/.env_vars, and do not run the skill with elevated privileges.

Risk: The documented npx install path depends on installer code outside the skill artifact.

Mitigation: Pin or review the installer version before using the npx path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vst93/skills/vision-fallback-skill)
- [Configuration](references/configuration.md)
- [API Reference](references/api-reference.md)
- [Output Format](references/output-format.md)
- [Constraints and Escalation](references/constraints.md)
- [Security](SECURITY.md)
- [Volcengine Ark documentation](https://www.volcengine.com/docs/82379)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Structured JSON object with summary, objects, text_detected, ui_structure, inferred_elements, and uncertainty_notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Consumes an image path, URL, or data URL plus optional OCR text, failure reason, and primary model output; requires a configured API key and vision endpoint.]

## Skill Version(s):

1.4.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
