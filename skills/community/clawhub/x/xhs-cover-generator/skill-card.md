## Description:

This skill helps Xiaohongshu creators analyze recent high-performing cover examples and generate practical cover design directions, sample-backed summaries, and image prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[if530770](https://clawhub.ai/user/if530770)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, brand operators, agencies, and MCN teams use this skill to turn a Xiaohongshu topic or draft into cover-analysis reports and practical cover design prompts backed by recent platform trend data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and campaign themes are sent to onetotenvip.com.

Mitigation: Use only keywords acceptable to share with that third-party service and disclose this network dependency to users before execution.

Risk: The skill retrieves and displays unvalidated remote cover image URLs.

Mitigation: Apply URL allowlisting, request limits, and link review before rendering images or following returned links.

Risk: The helper script uses custom no-SNI TLS behavior with certificate validation disabled.

Mitigation: Replace it with standard HTTPS certificate validation before routine deployment and run the current script only in a constrained environment.

## Reference(s):

- [Core workflow](references/core_workflow.md)
- [Xiaohongshu trend data format](references/xhs_trend_data_format.md)
- [ClawHub skill page](https://clawhub.ai/if530770/skills/xhs-cover-generator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports, JSON data from the helper script, and cover image prompts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include third-party image URLs and Xiaohongshu post or profile links returned by the data source.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
