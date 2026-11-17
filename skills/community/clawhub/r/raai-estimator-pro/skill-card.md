## Description:

Construction estimating for the Russian market: local estimates, BOQ, KS-2, KS-3, defect inspection, material calculation and estimate audit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raaipro](https://clawhub.ai/user/raaipro)

### License/Terms of Use:

MIT-0

## Use Case:

External construction teams, estimators, foremen, customers, contractors, and developers use this skill to draft Russian-market estimates, bills of quantities, material calculations, KS-2/KS-3 documents, tender proposals, and estimate audits.

### Deployment Geography for Use:

Russia

## Known Risks and Mitigations:

Risk: Generated prices, Russian norms, KS-2/KS-3 forms, and audit recommendations may be outdated or inaccurate.

Mitigation: Treat outputs as drafts and verify them against current official sources with a qualified estimator or legal/commercial reviewer.

Risk: Bundled helper shell scripts are reported as malformed.

Mitigation: Do not rely on the helper scripts until they are fixed and reviewed.

Risk: Weak input data such as missing measurements, unclear work scope, or missing region can make estimates misleading.

Mitigation: Require measured volumes, work composition, region, pricing base, and relevant source documents before using outputs for decisions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/raaipro/skills/raai-estimator-pro)
- [README](README.md)
- [Anti-fail and limits](docs/anti-fail.md)
- [Onboarding](docs/onboarding.md)
- [ROI model](docs/roi.md)
- [Quick start examples](examples/quick-start.md)
- [Full example library](examples/full-library.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown tables and structured construction-estimate documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Russian-language estimating outputs; reliable use requires region, scope of work, measured volumes, and current official pricing inputs.]

## Skill Version(s):

3.5.4 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
