## Description:

Audits Unreal Engine projects for structure, baseline changes, logs, packaging readiness, and selected asset structure, then produces reports and an evidence bundle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miracle1814](https://clawhub.ai/user/miracle1814)

### License/Terms of Use:

Apache-2.0

## Use Case:

Unreal Engine developers use this skill to inspect project health, compare changes against a baseline, check logs and packaging readiness, and review selected asset structures. It produces assessment reports rather than certification or proof that no writes occurred.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Baseline output can overwrite existing files.

Mitigation: Use a fresh destination outside the project, check resolved paths, and keep backups.

Risk: Comparisons may miss changes involving filenames that differ only by case.

Mitigation: Independently verify important comparisons involving case-only filename differences.

Risk: Enabling PIE can have gameplay side effects.

Mitigation: Enable PIE only deliberately on trusted projects.

Risk: Live checks depend on a local editor bridge whose implementation was unavailable for review.

Mitigation: Use a trusted local bridge.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/miracle1814/skills/ue-audit)
- [Project homepage](https://github.com/miracle1814/ue-audit)
- [English README](artifact/references/README.en.md)
- [Checks and known limitations](artifact/references/CHECKS.md)
- [Security guidance](artifact/references/SECURITY.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, HTML, JUnit XML, Evidence files]

**Output Format:** [JSON, Markdown, HTML, JUnit XML, and an evidence bundle]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports distinguish pass, warn, fail, skip, and unknown; unknown means the item was not verified.]

## Skill Version(s):

0.4.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
