## Description:

Social media content scraping and automation skill. Supports real-time single post reading, as well as scheduled batch patrol, LLM distillation, and review notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hacksing](https://clawhub.ai/user/hacksing)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to fetch X/Twitter posts or articles for reading, discussion, reply drafting, and batch monitoring workflows. Pipeline mode can deduplicate watched posts, send content to a configured LLM provider, and present generated drafts for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL fetching and the local review server are under-protected enough that crafted input or local web content could read or change review data or trigger LLM calls.

Mitigation: Review before installing, use only trusted exact X/Twitter status URLs, and avoid running the review server while browsing untrusted sites.

Risk: Private, regulated, or sensitive content may be sent to configured fetch and LLM providers during processing.

Mitigation: Do not process private or regulated content unless the operator accepts that provider exposure; prefer a trusted fixed LLM endpoint and temporary API key.

Risk: URL validation and review API authentication are not fixed according to the security guidance.

Mitigation: Use local firewall or sandbox controls until URL validation and review API authentication are addressed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/hacksing/skills/social-reader)
- [Publisher profile](https://clawhub.ai/user/hacksing)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance]

**Output Format:** [Markdown guidance with Python and shell examples, plus JSON records for fetched posts, queues, drafts, and archives.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive fetches are stateless; pipeline mode writes local JSON state and may call a configured LLM endpoint.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
