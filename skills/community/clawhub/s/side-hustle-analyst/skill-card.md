## Description: <br>
Runs structured day-by-day execution for AI agent side hustles by tracking experiment state, enforcing approval gates, and logging outcomes across a 28-day workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asimons81](https://clawhub.ai/user/asimons81) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run the 28-day Agent Side Hustle School workflow, resume from saved state, and maintain daily experiment logs and summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and updates local workflow state and progress files. <br>
Mitigation: Install it only in a workspace intended for this 28-day workflow and review any existing course-state.json before use. <br>
Risk: Experiment choices, pricing, lock-in, or spending decisions could be acted on before the operator agrees. <br>
Mitigation: Require operator approval for experiment selection, Day 5 lock-in, offer definition and pricing, and any spend above $0. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/asimons81/side-hustle-analyst) <br>
- [Publisher profile](https://clawhub.ai/user/asimons81) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown daily summaries and experiment logs with local workflow state updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads state/course-state.json and writes output/experiment-log/ and output/daily-summaries/ when used by an agent.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
