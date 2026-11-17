## Description:

Generates five non-repeating WeChat Moments posts and matching hand-drawn education-themed illustrations for a SongshuAI study room, either on demand or on a daily schedule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keystone-shiqi](https://clawhub.ai/user/keystone-shiqi)

### License/Terms of Use:

MIT-0

## Use Case:

Study room operators use this skill to generate parent-facing social media copy and warm education-themed illustrations for daily WeChat Moments marketing. The skill can be triggered manually or by scheduled times throughout the day.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled generation may post at unexpected times if the cron schedule is not reviewed.

Mitigation: Review the configured daily schedule before enabling automated use.

Risk: Image generation uses a MiniMax or compatible image API that may create provider costs and data-handling exposure.

Mitigation: Confirm API pricing, provider data handling, and credential configuration before installing or running the skill.

Risk: The skill keeps a permanent local history file for duplicate avoidance.

Mitigation: Avoid including sensitive personal, student, or business details in generated prompts or stored history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keystone-shiqi/skills/ssai-dailymoments)
- [MiniMax image generation API endpoint](https://api.minimaxi.com/v1/image_generation)

## Skill Output:

**Output Type(s):** [text, files, configuration]

**Output Format:** [Plain text posts with generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces five posts per manual run; scheduled use sends one configured post at each scheduled time.]

## Skill Version(s):

1.3.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
