## Description:

Converts a user's natural language video idea into a structured Seedance 2.0 prompt using multimodal references, camera guidance, visual styles, known-issue workarounds, and generation settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wfhiew](https://clawhub.ai/user/wfhiew)

### License/Terms of Use:

MIT-0

## Use Case:

External users and video creators use this skill to turn Seedance 2.0 video ideas into complete prompts with mode selection, asset mapping, shot-by-shot direction, audio cues, negative constraints, and known-issue workarounds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad video-prompt requests where the user did not explicitly ask for Seedance 2.0.

Mitigation: Confirm the target generator or ask targeted setup questions before producing a Seedance-specific prompt.

Risk: Reference-asset uploads, culturally specific styles, language choices, and watermark removal can be inappropriate when they do not match the user's intent or rights.

Mitigation: Apply those prompt elements only when the user has supplied the relevant intent, assets, and rights context.

Risk: Prompts can accidentally invoke protected brands, franchise characters, or recognizable likenesses.

Mitigation: Use original descriptive traits instead of protected names, redesign signature features, and add negative constraints for inferable IP terms.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/wfhiew/skills/seedance-2-prompt-optimizer)
- [Seedance 2.0 Prompt Engineering Skill](artifact/SKILL.md)
- [Prompt Best Practices - Seedance 2.0](artifact/best-practices.md)
- [Camera Angles & Movement Reference - Seedance 2.0](artifact/camera-angles.md)
- [Common Issues & Workarounds - Seedance 2.0](artifact/common-issues.md)
- [Visual Styles Reference - Seedance 2.0](artifact/styles.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown structured prompt with asset mapping, shot descriptions, constraints, generation settings, and known-issue notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prompt-level safety constraints, reference-asset handling guidance, and mitigation notes for known Seedance 2.0 output issues.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
