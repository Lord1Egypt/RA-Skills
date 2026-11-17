## Description:

Use Renderful from OpenClaw for image/video/audio/3D creation with model discovery, quote-before-generate workflow, deterministic polling, and insufficient-funds/x402 fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luv005](https://clawhub.ai/user/luv005)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to discover Renderful models, quote media generation jobs before running them, generate image, video, audio, or 3D outputs, and poll generation status through terminal completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generation and webhook actions may incur cost or send data to Renderful.

Mitigation: Review quotes, payment requirements, and destination details before approving generation or webhook setup.

Risk: Insufficient funds or x402 payment requirements can interrupt generation.

Mitigation: Surface payment requirements, deposit addresses, shortfall details, or valid x_payment options before retrying.

## Reference(s):

- [Renderful homepage](https://renderful.ai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with structured tool-call steps and status handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quote-before-generate workflow with deterministic polling and payment fallback guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
