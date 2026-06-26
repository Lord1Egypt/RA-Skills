## Description: <br>
Plan cross-time-zone meeting windows for distributed teams, providing region-by-region local time mappings and tradeoff analysis for scheduling decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, and distributed-team coordinators use this skill to compare cross-time-zone meeting windows, map local times by region, and explain scheduling tradeoffs before sending calendar invites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduling output may be inaccurate for date-specific DST changes, regional aliases, or high-stakes calendar decisions. <br>
Mitigation: Treat recommendations as advisory, prefer precise IANA time zones, and manually confirm important meeting times before sending invites. <br>


## Reference(s): <br>
- [Time Zone Planner release page](https://clawhub.ai/aipoch-ai/time-zone-planner) <br>
- [Time Zone Planner - References](references/guidelines.md) <br>
- [Audit Reference](references/audit-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown recommendations with optional JSON-formatted scheduling output and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes assumptions, recommended windows, local-time mappings, tradeoffs, risks, and manual confirmation checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
