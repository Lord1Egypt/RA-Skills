## Description: <br>
Generates and submits weekly reports from Aliyun DevOps workitems through the EMOP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yaojiangfeng](https://clawhub.ai/user/yaojiangfeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or team operators use this skill to collect Aliyun DevOps workitems, summarize weekly progress, and submit current or backfilled reports to EMOP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read internal DevOps data and submit reports to EMOP. <br>
Mitigation: Show the exact report payload and confirm each submission before sending it. <br>
Risk: Backfill mode can create multiple weekly submissions if the date range is too broad. <br>
Mitigation: Set and confirm a clear backfill date range before running backfill mode. <br>
Risk: Browser-session fallback may use an authenticated DevOps session when direct API access fails. <br>
Mitigation: Use browser-session fallback only with explicit approval and after inspecting the referenced local scripts. <br>


## Reference(s): <br>
- [URLs and IDs](references/urls.md) <br>
- [Local scripts and entrypoints](references/cli.md) <br>
- [ClawHub skill page](https://clawhub.ai/yaojiangfeng/weekly-report-flow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, guidance] <br>
**Output Format:** [Markdown summary, HTML ordered list, and EMOP report payload] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses DEVOPS_TOKEN and EMOP_TOKEN from the environment; backfill mode can submit one report per missing week.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
