## Description:

Fetches WeChat public account articles from mp.weixin.qq.com links and saves them into Notion as structured pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[opoojkk](https://clawhub.ai/user/opoojkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to archive public WeChat articles into a Notion page or database while preserving article metadata, text blocks, and image positions where possible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can fetch a user-supplied URL broader than the stated WeChat-only purpose.

Mitigation: Use only trusted https://mp.weixin.qq.com/s/ article URLs and add strict URL validation that rejects redirects to other hosts or private addresses.

Risk: Parsed article content is uploaded to Notion through the configured integration.

Mitigation: Limit the Notion integration to the minimum pages or databases needed and document the data transfer before use.

Risk: The skill can save content into a Notion page or database without an explicit confirmation step.

Mitigation: Review inputs before execution and add a confirmation step before creating or appending Notion content.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration instructions, JSON]

**Output Format:** [Markdown guidance with inline bash commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Notion integration token and a target Notion page or database shared with the integration.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
