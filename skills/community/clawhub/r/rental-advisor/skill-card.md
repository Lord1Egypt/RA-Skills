## Description: <br>
Rental Advisor helps users evaluate rental areas, listings, rent ranges, and rental contract terms based on budget, commute, unit type, and other housing constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanghou2025](https://clawhub.ai/user/fanghou2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to compare rental areas, search listings, estimate rent, and review rental contract terms for major Chinese cities. It asks for required rental details, uses city references and live search when available, and presents advisory findings rather than final legal or financial decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may rely on broad web or shell-based listing searches, which can return unreliable public posts or expose the session to untrusted sources. <br>
Mitigation: Use trusted, scoped search tools, review sources before acting, and avoid unknown local helper scripts or unrestricted shell scraping. <br>
Risk: Rental profiles can include sensitive rent, location, budget, commute, and contract details. <br>
Mitigation: Do not save profile details or enable future alerts unless the user explicitly asks for retention; keep stored details minimal. <br>
Risk: Rental prices, listings, and contract assessments can be outdated or legally incomplete. <br>
Mitigation: Verify current listing data, landlord identity, payment requests, and important contract terms with authoritative sources or qualified professionals before paying or signing. <br>


## Reference(s): <br>
- [Rental Advisor ClawHub page](https://clawhub.ai/fanghou2025/rental-advisor) <br>
- [Beijing Area Reference](references/beijing.md) <br>
- [Guangzhou Area Reference](references/guangzhou.md) <br>
- [Rent Estimation Reference Guide](references/pricing.md) <br>
- [Shanghai Area Reference](references/shanghai.md) <br>
- [Shenzhen Area Reference](references/shenzhen.md) <br>
- [Rental Contract Review Detailed Checklist](references/checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown reports, checklists, and advisory summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responds in the user's language; rental guidance is advisory and may depend on live search availability.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
