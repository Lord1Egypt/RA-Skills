## Description: <br>
Performs comprehensive SEO audits of websites, analyzing technical SEO, on-page factors, content quality, performance indicators, and producing actionable reports with scores and recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eyensama](https://clawhub.ai/user/eyensama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Website owners, digital marketers, SEO agencies, freelancers, and other external users use this skill to audit website SEO health, compare sites, and produce prioritized improvement recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches user-supplied pages, robots.txt, and sitemap.xml, which can create unintended network access if pointed at private or internal sites. <br>
Mitigation: Use it only for public or explicitly authorized websites, and review target URLs before allowing the agent or shell helper to fetch them. <br>
Risk: The shell helper uses curl and writes temporary /tmp/seo_* files while collecting audit signals. <br>
Mitigation: Run the helper in an environment where outbound web requests and temporary local files are expected, and remove temporary audit files if retention is a concern. <br>
Risk: SEO recommendations may be incomplete because the skill evaluates page content and indicators rather than authoritative search-engine ranking data. <br>
Mitigation: Treat findings as reviewable guidance and validate high-impact changes with site analytics, webmaster tools, or a human SEO review. <br>


## Reference(s): <br>
- [SEO Best Practices Reference](references/seo-best-practices.md) <br>
- [SEO Audit Bot Demo Report](references/demo-report.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown SEO audit report with scores, findings, and prioritized recommendations; optional shell output from the audit helper.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include overall and section scores, technical checks, on-page SEO findings, content analysis, performance indicators, social/schema findings, and competitor comparison results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and README version section) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
