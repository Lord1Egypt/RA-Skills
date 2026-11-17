## Description:

Monitors Xiaohongshu posts about Meituan errands and related services, filters posts by keyword and date, classifies sentiment and feedback themes, and produces Markdown feedback reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinghuan2000](https://clawhub.ai/user/qinghuan2000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and product teams use this skill to monitor Xiaohongshu discussion of errand and delivery services, summarize sentiment, identify recurring complaints, and prepare Markdown reports for review or knowledge-base publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a logged-in browser session and save scraped social-media content locally.

Mitigation: Run it in an isolated browser profile, restrict CDP to a validated local endpoint, and store or delete scraped files according to the user's data-handling requirements.

Risk: The remote LLM classifier includes hardcoded authentication material and may send post content to a remote service.

Mitigation: Remove hardcoded credentials before use, rotate any exposed credentials, and disclose, approve, or disable remote LLM classification.

Risk: Scheduled runs or KM document edits could publish unreviewed or inaccurate analysis.

Mitigation: Require explicit approval before enabling scheduled execution or writing reports into KM documents.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qinghuan2000/skills/xhs-feedback-analyzer)
- [Publisher Profile](https://clawhub.ai/user/qinghuan2000)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown reports, JSON scrape/classification data, and command-line workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write scraped social-media data locally and may insert reviewed report text into a KM document when configured with browser CDP access.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
