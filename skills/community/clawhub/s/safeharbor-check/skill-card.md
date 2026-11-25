## Description:

Check a structured CSV against the HIPAA Safe Harbor identifier classes in 45 CFR 164.514(b)(2) — dates more precise than a year, ZIP codes longer than three digits, ages over 89, and columns holding names, phone numbers, SSNs, emails, URLs, IP addresses and the other classes (A) to (R). Use when asked to check a CSV for Safe Harbor identifiers, scan a dataset for HIPAA identifiers before sharing, or apply the mechanical Safe Harbor fixes (dates to year, ZIP to three digits, ages over 89 to 90+) to declared columns. Not for eGFR calculation (use egfr-batch), lab-unit conversion (use labunits), growth z-scores (use growthz), or randomisation lists (use blockrandom). A checker, not a certification; not legal advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raktikoo](https://clawhub.ai/user/raktikoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data stewards use this command-line tool to check structured CSV files for detectable HIPAA Safe Harbor identifier classes and, when they declare the columns, apply limited date, ZIP code, age, or column-removal transformations. Human review is still needed for content the tool cannot verify and before relying on results for data sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation uses pip to install from a GitHub repository, and the security scan does not independently establish the safety of that repository or its dependencies.

Mitigation: Review the repository and its dependencies before installing.

Risk: A clean mechanical report cannot establish that a dataset meets HIPAA Safe Harbor requirements; free text and some identifier classes cannot be verified mechanically.

Mitigation: Have a person familiar with the data review unverifiable content and confirm the dataset before real-world use; do not treat the result as certification or legal advice.

## Reference(s):

- [Project repository (referenced by the skill)](https://github.com/RakTikoo/safeharbor-check)
- [SafeHarbor Check on ClawHub](https://clawhub.ai/raktikoo/skills/safeharbor-check)

## Skill Output:

**Output Type(s):** [Text, CSV files]

**Output Format:** [Per-class text report and, when requested, a transformed CSV file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports detectable violations and unverifiable classes; applies only the declared transformations and columns.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
