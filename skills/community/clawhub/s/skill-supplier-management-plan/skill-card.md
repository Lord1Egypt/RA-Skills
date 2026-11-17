## Description:

Generates structured supplier management plans for supplier quality managers, covering classification, onboarding, performance evaluation, audits, change control, quality agreements, supplier development, and risk response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Supplier quality managers and procurement quality leaders use this skill to draft annual or category-specific supplier management plans with a consistent nine-part framework. It helps collect inputs, produce a reviewable outline, and generate plain-text and Markdown plan documents for internal circulation and archival.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs the agent to run a relative local script that is not included in the package evidence.

Mitigation: Confirm that scripts/build_report.py exists in the expected package path before running it; otherwise generate the plan without executing an unresolved workspace script.

Risk: The skill creates report files in the workspace and same-day filenames may overwrite prior drafts.

Mitigation: Confirm the output directory and check for existing files before writing; use unique filenames or backups for repeated runs.

Risk: Supplier thresholds and management decisions may be company-specific and unsuitable if filled with generic values.

Mitigation: Keep company-specific thresholds marked for enterprise completion and require management review before publishing the plan.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/duding-engicool/skill-supplier-management-plan)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-supplier-management-plan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text and Markdown supplier management plan documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill describes writing generated reports under ./out and asks users to fill enterprise-specific thresholds before release.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
