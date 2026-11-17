## Description:

Pick the right Runware model for a task and keep that choice current by helping an agent discover available models and check capabilities, status, and price before selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runware](https://clawhub.ai/user/runware)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to route Runware generation tasks to suitable live models by capability, modality, status, price, and quality needs. It is especially useful as a foundation skill for downstream Runware outcome skills that need current model-selection guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model catalog entries, status, pricing, or replacement metadata may change after a recommendation is made.

Mitigation: Verify the selected model's live status, capabilities, replacement metadata, and pricing against Runware's catalog before execution.

Risk: Separate Runware execution skills, CLIs, or SDK calls may trigger paid model runs or batch jobs.

Mitigation: Review execution configuration and perform a pricing check or dry run before high-volume generation.

## Reference(s):

- [Runware Models on ClawHub](https://clawhub.ai/runware/skills/runware-models)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with optional catalog lookup commands or tool-call recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Model recommendations should be verified against the live Runware catalog before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
