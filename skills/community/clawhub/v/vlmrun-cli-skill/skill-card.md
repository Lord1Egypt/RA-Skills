## Description:

Use the VLM Run CLI to work with Orion visual AI on images, videos, documents, and generated media through natural-language prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spillai](https://clawhub.ai/user/spillai)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to invoke the VLM Run CLI for visual AI chat, image and video analysis or generation, OCR, document extraction, and media summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input files may be uploaded to a remote VLM Run service.

Mitigation: Avoid sending confidential images, videos, PDFs, contracts, invoices, or other sensitive files unless the user accepts the service's handling of uploaded data.

Risk: Generated artifacts and processed files may be cached locally.

Mitigation: Clear or relocate the cache when working with private artifacts, and choose explicit output directories for sensitive work.

Risk: The setup command installs the external vlmrun CLI package.

Mitigation: Install in an isolated virtual environment and consider pinning or reviewing the vlmrun package version before use.

Risk: Continuing sessions can retain prior context and generated artifacts.

Mitigation: Start fresh sessions for sensitive tasks instead of reusing prior session IDs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spillai/skills/vlmrun-cli-skill)
- [VLM Run API endpoint](https://agent.vlm.run/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe CLI options, environment variables, session handling, JSON output mode, and artifact output directories.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
