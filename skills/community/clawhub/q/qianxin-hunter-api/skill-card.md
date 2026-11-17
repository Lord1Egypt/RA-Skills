## Description:

Qianxin Hunter API skill for Hunter search queries and export tasks, including batch queries, with the QIANXIN_HUNTER_API_KEY environment variable configured.

This skill is ready for commercial/non-commercial use.

## Publisher:

[piggyhurry](https://clawhub.ai/user/piggyhurry)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and security teams use this skill to run Qianxin Hunter searches, submit batch export jobs from query syntax or CSV targets, check task status, and download exported CSV results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hunter search queries and uploaded CSV targets are sent to hunter.qianxin.com.

Mitigation: Install only when that data sharing is acceptable, and review CSV targets before upload.

Risk: API keys or authenticated URLs may be exposed through copied commands, logs, or terminal output.

Mitigation: Configure QIANXIN_HUNTER_API_KEY through the approved skill configuration path, avoid sharing authenticated output, and rotate the key if it is exposed.

Risk: Downloaded Hunter export files can contain sensitive asset data.

Mitigation: Store downloaded CSV files as sensitive data and avoid unnecessary post-processing or sharing.

Risk: The documentation includes curl examples that disable TLS verification.

Mitigation: Use the script's documented command syntax instead of copying curl -k examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/piggyhurry/skills/qianxin-hunter-api)
- [Hunter search API reference](references/api.md)
- [Hunter batch query API reference](references/api_batch.md)
- [API key configuration reference](references/apikey_config.md)
- [Batch file template](references/batch_file_template.csv)
- [Hunter batch template download](https://hunter.qianxin.com/api/search/batch/template?type=api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON or CSV API outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results and task-status responses are printed as JSON; completed batch downloads are saved as CSV files.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
