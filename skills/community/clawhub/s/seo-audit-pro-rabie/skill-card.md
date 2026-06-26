## Description: <br>
SEO Audit Pro audits a user-provided website URL for technical SEO, on-page SEO, content signals, scoring, and optional keyword content briefs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rabierr](https://clawhub.ai/user/rabierr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and site owners use this skill to run a permissioned single-page SEO audit and turn the audit JSON into an actionable Markdown report. When a target keyword is provided, it also creates a content brief with search intent, outline, metadata drafts, and internal-link suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit script makes web requests to user-provided URLs, which can touch private or internal systems if misused. <br>
Mitigation: Run it only against sites you own or have permission to test, and avoid private or internal URLs. <br>
Risk: The report is a lightweight single-page SEO audit and can overstate coverage for Core Web Vitals or competitive content gaps. <br>
Mitigation: Treat findings as directional and verify performance, ranking, and competitive conclusions with dedicated SEO and analytics tools. <br>


## Reference(s): <br>
- [SEO Audit Report Template](references/report-template.md) <br>
- [Content Brief Template](references/content-brief-template.md) <br>
- [Scoring Rubric](references/scoring.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/rabierr/seo-audit-pro-rabie) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with a JSON audit result from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append a keyword content brief when a target keyword is provided.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
