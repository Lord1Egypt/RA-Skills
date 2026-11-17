## Description:

A lightweight Chinese-language student productivity assistant that imports class schedules, finds free study time, and generates review, exercise, and daily schedule plans around class commitments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

Students use this skill to manage course schedules, identify free self-study periods or likely study spaces, and generate study, exercise, and daily-summary plans around class time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores class schedules, exam details, preferences, and generated plans in local memory/student JSON files.

Mitigation: Install only if local retention of this student data is acceptable, use clear fixed commands for write actions, and remove the stored files when the data is no longer needed.

Risk: Classroom and weather-dependent suggestions may be generic or based on defaults when live campus or weather data is unavailable.

Mitigation: Verify classroom availability, weather, and time-sensitive recommendations before relying on them for real-world planning.

## Reference(s):

- [Planning Algorithms Reference](references/planning-algorithms.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Concise Chinese Markdown/text summaries plus local JSON schedule and plan files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes student schedule, exam, review-plan, sport-plan, and optional preference data under local memory/student files.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
