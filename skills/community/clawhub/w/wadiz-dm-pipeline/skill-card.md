## Description: <br>
Crawls Wadiz and Tumblbug funding projects, filters makers at 50-99% funding progress, analyzes project text, and drafts personalized outreach DMs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thedalbee](https://clawhub.ai/user/thedalbee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Growth and marketing operators use this skill to collect eligible crowdfunding projects and prepare draft Korean DM outreach for maker prospects. It supports local review workflows by producing CSV rows with project details and generated message text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill crawls public crowdfunding pages and may be affected by platform terms, anti-spam expectations, or rate limits. <br>
Mitigation: Run it only where crawling and outreach are permitted, keep request volume conservative, and review platform rules before using generated prospects. <br>
Risk: When ANTHROPIC_API_KEY is set, scraped public project text may be sent to Anthropic to draft personalized messages. <br>
Mitigation: Unset ANTHROPIC_API_KEY for template-only generation, or confirm the data sharing posture is acceptable before enabling API-backed drafting. <br>
Risk: Generated DMs are outreach drafts and may be inaccurate, unsuitable, or non-compliant if sent without review. <br>
Mitigation: Review every CSV row and message manually, adjust claims and tone, and follow applicable anti-spam and marketing consent rules before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thedalbee/wadiz-dm-pipeline) <br>
- [DM template](references/dm-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions and generated CSV files containing project metadata and draft DM text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Playwright/Chromium setup; uses template-only generation unless ANTHROPIC_API_KEY is set.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
