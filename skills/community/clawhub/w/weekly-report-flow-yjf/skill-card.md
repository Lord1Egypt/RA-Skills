## Description: <br>
Generate and submit weekly reports from Aliyun DevOps workitems via EMOP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yaojiangfeng](https://clawhub.ai/user/yaojiangfeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers use this skill to turn Aliyun DevOps work items into weekly status summaries and submit them to EMOP. It also supports backfilling missing weekly reports for selected Friday report dates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read internal DevOps work items and send weekly report content to EMOP. <br>
Mitigation: Use it only when EMOP is an approved destination, keep tokens least-privilege, and review report content before submission. <br>
Risk: Weak confirmation around submissions or backfill ranges could post unintended weekly reports. <br>
Mitigation: Explicitly confirm the target Friday date or backfill range and require review before each EMOP POST. <br>
Risk: Referenced local scripts may perform actions outside the visible skill text. <br>
Mitigation: Inspect local scripts before running them and avoid writing DevOps or EMOP tokens to disk. <br>


## Reference(s): <br>
- [URLs / IDs](references/urls.md) <br>
- [Local scripts / entrypoints](references/cli.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown plus HTML ordered-list report content and API submission details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses environment-supplied DevOps and EMOP tokens; backfill mode produces one report per missing week.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
