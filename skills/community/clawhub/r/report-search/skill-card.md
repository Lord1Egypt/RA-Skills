## Description:

Searches and retrieves research reports, industry reports, company research, macro strategy, financial reports, and prospectuses from fxbaogao.com using keyword, organization, author, and date filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eliauktm](https://clawhub.ai/user/eliauktm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find fxbaogao.com research reports by keyword, publisher organization, author, or time range, then retrieve selected report summaries and content for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and selected document IDs are sent to fxbaogao.com.

Mitigation: Use only search terms and report identifiers appropriate to share with fxbaogao.com.

Risk: Disabling TLS verification can allow intercepted or misleading report data.

Mitigation: Keep TLS verification enabled; use FXBAOGAO_SSL_NO_VERIFY=1 only for short local troubleshooting.

Risk: Network or DNS restrictions can prevent report search or retrieval.

Mitigation: Allow outbound access to api.fxbaogao.com and www.fxbaogao.com when deploying the skill.

## Reference(s):

- [Fxbaogao API endpoint](https://api.fxbaogao.com)
- [Fxbaogao report view](https://www.fxbaogao.com/view?id=DOC_ID)
- [ClawHub skill page](https://clawhub.ai/eliauktm/skills/report-search)
- [Publisher profile](https://clawhub.ai/user/eliauktm)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown summaries with JSON-backed report metadata and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results preserve doc_id, organization, authors, publish date, and report links; detail responses prioritize summary sections before longer content.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
