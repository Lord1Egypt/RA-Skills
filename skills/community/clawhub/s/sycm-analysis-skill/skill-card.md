## Description:

Taobao Sycm (Business Advisor) data analysis tool for retrieving weekly store business reports, generating business insights, and fetching Sycm data for a Taobao store after the user is logged into sycm.taobao.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simoncai519](https://clawhub.ai/user/simoncai519)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve authenticated Taobao Sycm weekly store reports and turn the returned Markdown report into business analysis. It is intended for trusted workspaces because the report may contain sensitive store analytics and links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The returned weekly report can contain sensitive Taobao store analytics and business links.

Mitigation: Use the skill only in trusted workspaces and review report content before sharing it outside the intended audience.

Risk: The skill depends on the user's authenticated sycm.taobao.com session and may prompt for login if the session is missing or expired.

Mitigation: Complete login only through the official Taobao Sycm login flow and avoid running the skill where browser session access is not intended.

Risk: Rapid repeated requests to Sycm endpoints may trigger service security controls or rate limits.

Mitigation: Keep the documented 5-second polling interval and stop after the documented timeout if no report content is available.

## Reference(s):

- [Workflow Details](artifact/references/workflow.md)
- [ClawHub Skill Page](https://clawhub.ai/simoncai519/skills/sycm-analysis-skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report content with preserved charts and links, plus concise user guidance for login, retry, busy-system, and timeout states.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated sycm.taobao.com browser session; polling should use at least a 5-second interval and stop after about 5 minutes if no report content is returned.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
