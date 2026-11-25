## Description:

Analyzes close-up pet images or videos for eye redness, abnormal tearing, and corneal or pupil opacity, then provides visual anomaly alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners, boarding staff, and veterinary teams can use the skill to review close-up pet eye images or videos for visible signs that may warrant attention. Its output is a visual screening aid and does not replace a veterinarian's diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review rates the skill suspicious for account and credential handling, broad credential forwarding, and possible media uploads beyond its stated analysis purpose.

Mitigation: Follow the security guidance: avoid installation until credential handling, account behavior, and external media transfers have been clarified.

Risk: Visual screening results may be mistaken for a veterinary diagnosis.

Mitigation: Treat results as visual alerts only and consult a veterinarian about suspected abnormalities.

## Reference(s):

- [API reference](references/api_doc.md)
- [Analysis API reference](skills/smyx_analysis/references/api_doc.md)
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-eye-anomaly-detection-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured eye analysis report as readable text or JSON; Markdown table for history lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include anomaly alerts, suggestions, and report links; visual screening only, not a veterinary diagnosis.]

## Skill Version(s):

1.0.15 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
