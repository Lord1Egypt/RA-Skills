## Description:

Security-camera video annotation skill for extracting key frames, analyzing scene content, producing structured environment/person/behavior/risk annotations, and generating VL fine-tuning data in dataset.jsonl format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aowind](https://clawhub.ai/user/aowind)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and dataset builders use this skill to turn security-camera videos into structured VL model fine-tuning records. It supports frame extraction, per-video scene annotation, risk labeling, and dataset.jsonl assembly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security-camera videos, extracted frames, and generated training records may contain sensitive information about people, children, elderly persons, homes, or workplaces.

Mitigation: Use the skill only for intended datasets, review input and output directories before running it, and handle generated files according to the data owner's privacy and retention requirements.

Risk: The local workflow creates frame images and dataset files in user-selected output locations.

Mitigation: Confirm output paths before execution and inspect generated manifests and dataset records before sharing or using them for fine-tuning.

## Reference(s):

- [System Prompt Template](references/system-prompt.md)
- [Labels and Risk Level Reference](references/labels-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/aowind/skills/sjht-cam-anno)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON/JSONL file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces frame images, manifest.json, structured annotations, and dataset.jsonl records for video-based VL fine-tuning workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
