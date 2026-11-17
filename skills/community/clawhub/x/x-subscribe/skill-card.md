## Description:

Subscribes to selected X (Twitter) accounts, pulls their recent posts on a daily 9:00 schedule, and produces grouped reports with engagement data and AI summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External teams, creators, researchers, and marketing operators use this skill to subscribe to X accounts, monitor posts from selected handles or ranked account lists, and receive daily grouped reports for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Redfox API key to access the X account data APIs.

Mitigation: Provide the key through the REDFOX_API_KEY environment variable, confirm its source and revocation path, and avoid placing it in prompts, logs, code, or report output.

Risk: Daily 9:00 scheduled report tasks can continue collecting and summarizing selected public X accounts after setup.

Mitigation: Review the subscribed account list and scheduled task prompts before enabling or updating automation, and remove tasks or handles that are no longer needed.

Risk: Generated JSON and HTML reports may contain account activity, summaries, and engagement data stored on the local device.

Mitigation: Store report files only in appropriate local locations and delete or restrict access to reports that should not be retained.

Risk: HTML report export features can load third-party CDN scripts for PDF or image export and may auto-open the generated report in a browser.

Mitigation: Use the no-open option or avoid export features when CDN loading or automatic browser preview is not acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/x-subscribe)
- [API technical reference](references/api_docs.md)
- [Category configuration](assets/category_config.json)
- [Redfox API key settings](https://redfox.hk/settings/api-keys?source=clawhub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown summaries, shell command invocations, JSON data files, and HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a REDFOX_API_KEY environment variable; generated reports may be stored locally and opened in a browser.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
