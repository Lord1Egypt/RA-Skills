## Description:

Reverse-engineer AI video prompts from any video or screenshot. Analyzes shot types, camera movements, lighting, color grading, and director style. Outputs structured prompts for Kling, Seedance, Runway, Veo, Sora, Pika, HappyHorse and more. Includes full reproduction workflow. Use when user provides a video link, screenshot, or description and wants to replicate its style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chang9852](https://clawhub.ai/user/chang9852)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, developers, and video production teams use this skill to analyze a supplied video, screenshot, link, or style description and produce structured prompts and reproduction workflows for AI video tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HappyHorse prompt guidance may steer prompts toward Chinese when the user expects the original language to be preserved.

Mitigation: Confirm the desired output language before applying model-specific prompt language recommendations.

Risk: Model and style attribution produced from user-provided media may be uncertain.

Mitigation: Present model identification as an estimate and have the user review it before using it as provenance or production guidance.

## Reference(s):

- [Video AI Models & Cinematography Reference](references/model_params.md)
- [ClawHub skill page](https://clawhub.ai/chang9852/skills/video-prompt-reverse-engineer)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown with structured prompt sections, shot breakdowns, parameter tables, and reproduction workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model estimates, positive and negative prompts, camera prompts, style prompts, lighting prompts, and tool-specific parameter guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
