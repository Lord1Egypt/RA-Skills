## Description: <br>
Company Intel helps agents research prospective companies, identify relevant contacts, validate email candidates, create local prospect dossiers, and prepare OKKI CRM entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjboy007](https://clawhub.ai/user/cjboy007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and business-development users can use this skill to evaluate target companies, prioritize leads, draft outreach, and prepare structured company/contact records for follow-up. It is intended for reviewed prospecting workflows where users confirm collected contact data and CRM writes before relying on them. <br>

### Deployment Geography for Use: <br>
Global, subject to applicable sanctions, privacy, anti-spam, and CRM compliance requirements. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can infer and validate individual email addresses, including through active SMTP probing. <br>
Mitigation: Use only when authorized and legally appropriate; prefer review-only workflows and avoid live SMTP probing unless there is a clear lawful basis. <br>
Risk: The skill can store contact dossiers locally and prepare or write records to OKKI. <br>
Mitigation: Require human confirmation before CRM writes and define retention and deletion rules for generated company and contact records. <br>
Risk: Prospecting conclusions may rely on public-source inferences about companies, contacts, and timing. <br>
Mitigation: Review source evidence, preserve uncertainty in the output, and avoid acting on unsupported or sensitive conclusions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cjboy007/shadow-company-intel-scout) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown reports with structured tables, contact lists, scoring rationale, outreach drafts, and CRM-ready records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local dossier files and batch summary reports; CRM writes and contact validation should be reviewed before execution.] <br>

## Skill Version(s): <br>
2.0.0 (source: server evidence release version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
