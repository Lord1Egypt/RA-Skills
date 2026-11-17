## Description:

Running Coach helps runners generate percentage-based weekly training plans, prepare pre- and post-workout reviews, and optionally upload workouts to Intervals.icu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[popstarxu-spec](https://clawhub.ai/user/popstarxu-spec)

### License/Terms of Use:

MIT-0

## Use Case:

Runners and coaches use this skill to generate weekly run workouts, pace guidance, and workout review templates, with optional sync to Intervals.icu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The upload script can create or update workouts in the user's Intervals.icu training calendar.

Mitigation: Run with --dry-run first and review generated workouts before uploading.

Risk: The skill requires an Intervals.icu API key and athlete ID for uploads.

Mitigation: Prefer environment variables, avoid committing a populated config.json, and rotate the API key if it is exposed.

Risk: Generated training guidance may not fit the runner's current recovery, injury status, or goals.

Mitigation: Review the pre-workout state assessment and modify or skip sessions when fatigue, soreness, or other risk signals are present.

## Reference(s):

- [Running Coach ClawHub Skill Page](https://clawhub.ai/popstarxu-spec/skills/runningcoach)
- [Intervals.icu](https://intervals.icu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce dry-run previews or upload workout plans to Intervals.icu when credentials are configured.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
