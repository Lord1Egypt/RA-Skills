## Description:

Generate images via Google Cloud Vertex AI generateContent using Application Default Credentials (ADC).

This skill is ready for commercial/non-commercial use.

## Publisher:

[neogeosnk](https://clawhub.ai/user/neogeosnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to generate image files from prompt text through Google Cloud Vertex AI with Application Default Credentials. It is intended for workflows that can provide a Google Cloud project, local prompt file, and output path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Google Cloud bearer tokens could be exposed if response-supplied download URLs are not constrained to trusted Google endpoints.

Mitigation: Use low-privilege Google Cloud credentials and ensure bearer tokens are only sent to trusted Google endpoints.

Risk: Sensitive prompts or full API responses may be retained temporarily in debug artifacts.

Mitigation: Use non-sensitive prompts unless debug logging is explicit, necessary, and cleaned up after the request cycle.

Risk: The skill requires shell execution, environment access, and file access to run gcloud, curl, and the image harness.

Mitigation: Review before installing and run it in a constrained environment with only the project and file permissions needed for image generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neogeosnk/skills/vertex-image-adc)
- [Google Cloud Vertex AI](https://cloud.google.com/vertex-ai)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Configuration instructions]

**Output Format:** [Image file written to the requested output path with JSON status from the harness.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Google Cloud SDK, curl, a prompt file, a Google Cloud project, and ADC or user-token authentication.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
