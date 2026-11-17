## Description:

Fetches the registered author and influencer list for a XingTu recruitment task, paginates through the XingTu author-list API, and exports the results to a formatted Excel file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juanjuan2538](https://clawhub.ai/user/juanjuan2538)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to collect registered XingTu task authors for recruitment review, creator outreach, and campaign operations. It handles cookie-based access, paginated retrieval, and Excel export of author profile, pricing, status, and contact fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A live XingTu session cookie is provided to the agent and stored in plaintext.

Mitigation: Use a narrow session when possible, provide the cookie only in an environment where agent access is acceptable, and delete ~/.xingtuCookie.txt after the export is complete.

Risk: The generated Excel workbook may contain third-party contact and business information.

Mitigation: Treat the workbook as sensitive, limit distribution, and store or delete it according to the user's data-handling requirements.

Risk: An expired or invalid cookie can cause failed or partial retrieval.

Mitigation: Validate the cookie before export and require re-login when validation fails or the API reports an authentication error.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juanjuan2538/skills/xingtutaskauthor)
- [XingTu login](https://sso.oceanengine.com/xingtu/login?role=7)
- [XingTu task author list API](https://www.xingtu.cn/gw/api/challenge/provider_get_task_author_list)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Markdown, JSON]

**Output Format:** [Formatted Excel workbook with progress text and a JSON summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The default file name is xingtu_authors_<task_id>_<timestamp>.xlsx; output may include sensitive author contact and business information.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
