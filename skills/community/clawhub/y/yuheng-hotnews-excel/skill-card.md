## Description:

Processes uploaded hotspot-news Excel files by parsing sheets, extracting and summarizing topical news, saving JSON data, and producing categorized Markdown summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horizoncove](https://clawhub.ai/user/horizoncove)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to process Excel files whose names contain hotspot-news indicators, convert sheet data into retained JSON, and receive categorized summaries of key topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes persistent daily cron execution of an unaudited script outside the package.

Mitigation: Require explicit opt-in for scheduling and verify that /workspace/scripts/read_hotnews.py is controlled and reviewed before enabling it.

Risk: Recurring processing can retain generated output and logs beyond the user's immediate request.

Mitigation: Define output and log retention locations before use, and provide a clear way to disable the scheduled task and delete generated files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/horizoncove/skills/yuheng-hotnews-excel)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown summaries and JSON files with bash and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save dated JSON output under /workspace/data and can configure recurring cron execution when explicitly enabled.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
