## Description:

Generate and submit weekly reports from Aliyun DevOps workitems via EMOP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaojiangfeng](https://clawhub.ai/user/yaojiangfeng)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and workflow operators use this skill to collect Aliyun DevOps workitems, summarize weekly progress in Chinese, and submit the report to EMOP. It also supports backfilling missing weekly reports by Friday date.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses environment tokens to access Aliyun DevOps and EMOP.

Mitigation: Run it only in an environment where DEVOPS_TOKEN and EMOP_TOKEN are intended for this workflow, and keep those tokens out of files and logs.

Risk: Submitting a report changes an external business system.

Mitigation: Review the assignee, target project, report week, generated content, and EMOP endpoint before allowing submission or backfill runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yaojiangfeng/skills/weekly-report-flow-yjf)
- [URLs / IDs](artifact/references/urls.md)
- [Local scripts / entrypoints](artifact/references/cli.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, API calls, Shell commands, Guidance]

**Output Format:** [Markdown and HTML ordered-list report content, with API request guidance and optional shell/script entrypoints.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 200-300 Chinese characters for the weekly summary and submits one report per week in backfill mode.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
