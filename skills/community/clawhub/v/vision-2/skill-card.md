## Description:

Vision lets agents without native vision support analyze, describe, compare, and extract text from local or remote images through a configured OpenAI-compatible vision API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guorui999](https://clawhub.ai/user/guorui999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to add image understanding workflows to agents that otherwise cannot inspect images, including screenshot analysis, OCR-style text extraction, image description, and multi-image comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image content, OCR text, screenshots, prompts, and API credentials may be sent to the configured external vision provider.

Mitigation: Use only approved providers and HTTPS endpoints, avoid submitting sensitive images unless permitted, and review provider data-handling terms before deployment.

Risk: The installer supports remote URL downloads and the documented install path includes command-line installation flows that may introduce supply-chain risk.

Mitigation: Install from a pinned, reviewed release or local artifact rather than remote curl-pipe-to-bash flows, and verify file hashes before deployment.

Risk: The API key can be stored in a plaintext config file.

Mitigation: Prefer environment-based secret handling where available or restrict config file permissions when local storage is required.

## Reference(s):

- [Server-resolved GitHub repository](https://github.com/guorui999/vision)
- [ClawHub skill page](https://clawhub.ai/guorui999/skills/vision-2)
- [Aliyun Bailian console](https://bailian.console.aliyun.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown returned from the configured vision model, with setup and usage guidance expressed as shell commands and configuration values.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports local image files and remote image URLs; sends image content and prompts to the configured vision provider and requests up to 1024 output tokens.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
