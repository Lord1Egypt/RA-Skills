## Description:

Drafts structured radiology reports aligned to ACR RADS lexicons, with lexicon-controlled findings and an unsigned attending sign-out block for radiologist review before clinical action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Radiologists, fellows, residents, and radiology PAs/RAs use this skill to convert findings, technique details, and comparisons into draft structured reports aligned with applicable RADS lexicons for attending review before clinical action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Draft report content may be incorrect, incomplete, or clinically inappropriate if used without professional review.

Mitigation: Treat outputs as drafts only and require a qualified radiologist to review, edit, and sign out the report before clinical use.

Risk: Users may provide patient names, MRNs, DOBs, SSNs, full dates of service, or other unnecessary identifiers.

Mitigation: Use accession numbers or de-identified identifiers only, and handle accession numbers according to institutional policy.

Risk: Critical-result communication details may be missing from a draft.

Mitigation: Require the radiologist to complete recipient, time, mode, and read-back details before finalizing any critical-result report.

## Reference(s):

- [Structured Rads Report Drafter on ClawHub](https://clawhub.ai/archlab-space/skills/structured-rads-report-drafter)
- [Open-Skill-Hub Issues](https://github.com/archlab-space/Open-Skill-Hub/issues)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown draft structured radiology report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft only; avoids unnecessary patient identifiers and requires qualified radiologist review before clinical use.]

## Skill Version(s):

0.1.1 (source: server release metadata and artifact/CHANGELOG.md, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
