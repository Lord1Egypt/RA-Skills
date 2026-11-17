## Description:

Helps production supervisors and quality engineers identify, label, verify, and trace manufacturing change points across 4M/4M1E categories to reduce the risk of mass defects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

External manufacturing teams use this skill to structure change-point control during production preparation, shift handoff, first-article checks, and process monitoring. It guides users to classify changes, record risk and verification status, and produce traceable change-point ledgers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the generated ledger as an authoritative engineering or quality approval record.

Mitigation: Use the output as a procedural checklist and record template; require responsible quality or engineering personnel to make final verification and release decisions.

Risk: The artifact references a report-building script that is not included in the package.

Mitigation: Review generated ledger content directly, and confirm any local automation exists and is approved before relying on scripted report generation.

Risk: Generic high, medium, and low risk labels may not match a specific site's approved change-control thresholds.

Mitigation: Map the suggested risk level to the organization's formal change-control criteria before release or cross-shift tracking.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/duding-engicool/skills/skill-change-point-management)
- [Server-Resolved GitHub Provenance](https://github.com/duding-engicool/skill-change-point-management)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Plain text and Markdown change-point management ledgers with traceability IDs, risk levels, verification plans, verification conclusions, owners, and status fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Missing required fields are marked as pending rather than fabricated; release evidence notes that the referenced report-building script is not included in the package.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
