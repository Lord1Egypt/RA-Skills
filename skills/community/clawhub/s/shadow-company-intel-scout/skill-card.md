## Description:

Researches companies and contacts, validates candidate emails, creates sales-intelligence records, and generates lead scoring and outreach guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjboy007](https://clawhub.ai/user/cjboy007)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and business development users use this skill to build company intelligence dossiers, identify potential contacts, validate candidate emails, create CRM records, and draft follow-up messaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs lead enrichment involving personal contact records.

Mitigation: Use it only with authorization and a lawful basis, and define retention and deletion controls for collected contact data.

Risk: The skill can perform active SMTP email probing.

Mitigation: Avoid raw SMTP probing unless the organization has approved it; require a compliant email-validation method where approval is absent.

Risk: The skill can write customer and contact records into OKKI.

Mitigation: Require explicit confirmation before any OKKI write and review records for accuracy before submission.

Risk: The security evidence notes weak safeguards around local files and contact records.

Mitigation: Validate filenames and email addresses before writing files or records, and restrict local storage access to authorized users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cjboy007/skills/shadow-company-intel-scout)
- [Reasoning layer requirements](artifact/specs/reasoning-layer-requirements.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, local Markdown files, contact lists, CRM record payloads, and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local company dossier files and summary reports, and may write contact or customer records to OKKI when authorized.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
