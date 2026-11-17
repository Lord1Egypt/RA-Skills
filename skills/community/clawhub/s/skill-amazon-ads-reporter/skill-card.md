## Description:

Fetches Amazon Ads Sponsored Products campaign and keyword reports, including keyword performance analysis and live bid inspection, using user-provided Amazon Ads credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Advertisers, operators, and marketing analysts use this skill to configure and run Amazon Ads API reporting scripts that inspect Sponsored Products campaign performance, keyword winners and dead keywords, and current keyword bids.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Amazon Ads API credentials from a local JSON file.

Mitigation: Install only when Amazon Ads API access is intended, keep the credential file protected, and set AMAZON_ADS_PATH deliberately when the default path should not be used.

Risk: Some documented campaign-level commands reference scripts not included in this artifact.

Mitigation: Verify the available scripts before using campaign-level examples; this artifact includes keyword-report.js and get-bids.js.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with bash commands and console or table report output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads Amazon Ads credentials from a local JSON file and can produce local JSON report files or live keyword bid listings.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
