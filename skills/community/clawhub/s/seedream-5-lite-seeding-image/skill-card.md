## Description:

Helps creators use Seedream 5.0 Lite through AI Hive to create recommendation visuals that separate visible facts, creator judgments, and claims requiring proof while reserving space for sponsorship and AI-synthesis disclosures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and agent operators use this skill to produce product recommendation visuals from authorized materials while keeping visible product facts separate from creator experience claims and brand claims that require proof.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A compromised service response could overwrite files outside the intended output folder during downloads.

Mitigation: Run the helper from a low-privilege account, choose an isolated output directory, review downloaded paths, and fix filename handling before production use.

Risk: Reference images are uploaded to AI Hive for generation.

Mitigation: Use only images that the operator is authorized to upload and retain the source records required by the release checklist.

Risk: Unpinned dependencies can change behavior between installs.

Mitigation: Pin and review dependencies before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedream-5-lite-seeding-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, image files, guidance]

**Output Format:** [Markdown guidance with bash examples, CLI status output, JSON task data, and downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the fixed public_model_seedream_5_0_lite image model, accepts optional authorized reference images, and can save generated results to a chosen output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
