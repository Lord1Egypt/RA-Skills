## Description:

Complete Venice AI API toolkit for image generation, video, audio, embeddings, transcription, characters, models, and admin functions with privacy-focused inference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sabrinaaquino](https://clawhub.ai/user/sabrinaaquino)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to call Venice AI API capabilities from an agent workflow, including media generation, transcription, embeddings, model and character discovery, account balance checks, usage reporting, rate-limit checks, and API-key administration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, files, audio, images, and account data selected by the user are sent to Venice AI.

Mitigation: Install only if you trust Venice AI with that data, and avoid sending sensitive inputs that should not leave your environment.

Risk: Admin commands can access billing, usage, rate limits, and API-key management functions.

Mitigation: Use an inference key for normal generation and transcription work, and reserve admin keys for explicit account administration tasks.

Risk: API-key creation can print a newly created full key to the terminal, where it may be captured in logs.

Mitigation: Avoid creating API keys in logged terminals and store newly created keys immediately in a secure secret manager.

Risk: The scripts rely on the httpx Python dependency resolved at runtime.

Mitigation: Pin or pre-approve httpx in sensitive environments before running the skill.

## Reference(s):

- [Venice AI](https://venice.ai)
- [Venice AI API Documentation](https://docs.venice.ai)
- [Venice API Base URL](https://api.venice.ai/api/v1)
- [PEP 723 Inline Script Metadata](https://peps.python.org/pep-0723/)
- [ClawHub Skill Page](https://clawhub.ai/sabrinaaquino/skills/venice-api-kit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON or CSV API responses, and saved image, audio, video, or transcription files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv, python3, httpx, and VENICE_API_KEY; admin commands require an admin Venice API key.]

## Skill Version(s):

2.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
