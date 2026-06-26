## Description: <br>
Helps agents use TimeCamp for timer status, time entries, task lookup, analytics, and reporting workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kamil-rudnicki](https://clawhub.ai/user/kamil-rudnicki) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and teams use this skill to manage TimeCamp timers and time entries, list tasks, fetch TimeCamp datasets, and produce time-tracking reports. It is also useful for authorized analytics over entries, users, tasks, application names, and computer activity data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive TimeCamp employee activity, user, and time-entry data. <br>
Mitigation: Use it only with authorization for the requested account and dataset, and avoid all-user or employee activity queries unless that access is approved. <br>
Risk: The TimeCamp API key grants account access and may be exposed if handled casually. <br>
Mitigation: Store TIMECAMP_API_KEY as a secret, avoid printing it, and treat command output and generated data files as sensitive. <br>
Risk: Write actions such as adding, updating, removing entries, or stopping timers can change TimeCamp records. <br>
Mitigation: Confirm the requested action with the user and show the command before executing modifications. <br>


## Reference(s): <br>
- [ClawHub TimeCamp Skill](https://clawhub.ai/kamil-rudnicki/timecamp) <br>
- [TimeCamp](https://www.timecamp.com) <br>
- [TimeCamp CLI Repository](https://github.com/timecamp-org/timecamp-cli.git) <br>
- [TimeCamp Data Pipeline Repository](https://github.com/timecamp-org/good-enough-timecamp-data-pipeline.git) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, SQL snippets, and JSONL-oriented reporting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TIMECAMP_API_KEY for TimeCamp access; fetched analytics data is written as JSONL by the referenced pipeline.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
