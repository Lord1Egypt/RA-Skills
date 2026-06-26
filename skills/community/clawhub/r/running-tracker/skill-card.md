## Description: <br>
Track, log, and analyze running workout times from casual run reports and answer questions about running history, pace, progress, personal bests, training advice, and logged running data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fdocr](https://clawhub.ai/user/fdocr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and runners use this skill to keep a local markdown log of workouts and ask for pace, speed, calorie estimates, trends, personal bests, and cautious projections from logged runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workout dates, distances, and times are retained in a local markdown file. <br>
Mitigation: Review or delete runs.md if you do not want workout data retained. <br>
Risk: Training advice and projections are based on logged run history and simple extrapolation. <br>
Mitigation: Treat projections as estimates and note assumptions when extrapolating to distances the user has not logged. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fdocr/running-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/fdocr) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown table updates and plain-language responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains a local runs.md table with distance, date, and time; estimates calories using 62 cal/km when logging runs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
