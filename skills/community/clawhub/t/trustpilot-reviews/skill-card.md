## Description: <br>
Trustpilot Reviews extracts paginated customer review records from public Trustpilot company pages using a company domain and optional filters for page, rating, language, verification status, replies, date range, keyword, and reviewer country. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operations teams can use this skill to collect structured Trustpilot review data for brand monitoring, competitor analysis, reporting, sentiment workflows, and review-response analysis. Users should confirm they have a lawful and compliant basis before collecting reviewer identifiers or profile metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports suspicious scraping posture because the skill encourages stealth/proxy, fingerprint-rotation, and rate-limit-avoidance instructions. <br>
Mitigation: Install only for a lawful, compliant review-data collection purpose and remove or ignore stealth, proxy, fingerprint-rotation, and rate-limit-avoidance guidance before use. <br>
Risk: The skill collects reviewer identifiers and profile metadata that may be personal data. <br>
Mitigation: Minimize collected fields, avoid lead-generation or profiling unless clearly authorized, and prefer official export, API, or permissioned access for bulk work. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/browseract-cli/skills/trustpilot-reviews) <br>
- [Trustpilot Public Review Page Pattern](https://www.trustpilot.com/review/{domain}) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON review records with pagination, active filter, company context, and scrape timestamp fields; guidance may include shell commands for browser-act execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include optional reviewer metadata, reply analysis dates, extended review metadata, review photo URLs, and client-side country filtering.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
