## Description: <br>
Running Coach helps runners generate percentage-based weekly training plans, pace-zone guidance, and pre- or post-workout reports, with optional synchronization to Intervals.icu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[popstarxu-spec](https://clawhub.ai/user/popstarxu-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Runners and coaching agents use this skill to plan weekly running workouts, compute pace zones from a threshold pace, prepare workout readiness and review reports, and optionally upload planned workouts to an Intervals.icu calendar. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Intervals.icu API credentials. <br>
Mitigation: Store credentials in environment variables or a secret manager, avoid committing config.json with secrets, and rotate credentials if exposed. <br>
Risk: The skill can modify live training-calendar data. <br>
Mitigation: Run with dry-run mode first and require explicit confirmation before upload, update, bulk operation, or delete actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/popstarxu-spec/runningcoach) <br>
- [Intervals.icu](https://intervals.icu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples plus structured workout data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can read Intervals.icu credentials from environment variables or config.json and can perform dry-run or live workout uploads.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
