## Description:

Analyzes post-feeding fish videos to estimate feeding activity, remaining feed, and appetite alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Aquarium keepers and aquaculture operators can use the skill to turn post-feeding camera footage into feeding activity summaries, remaining-feed estimates, and alerts for closer observation. The results support monitoring and should not be treated as a disease diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags unclear account registration and credential handling.

Mitigation: Avoid installing or running the skill with production credentials until the operator clarifies how accounts and credentials are handled.

Risk: The security review flags video transfer disclosures and possible cross-user history exposure.

Mitigation: Until transfer destinations, access boundaries, and retention are clarified, use only non-sensitive test footage in an isolated environment.

Risk: The security review reports that parts of the supplied implementation may not match the fish-analysis description, including export-only behavior.

Mitigation: Confirm the actual analysis, data handling, and export behavior before relying on scores or alerts.

## Reference(s):

- [Fish feeding analysis API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release](https://clawhub.ai/18072937735/skills/smyx-fish-feeding-activity-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Structured data, Markdown, Guidance]

**Output Format:** [Structured feeding report with activity scores, alerts, recommendations, and report links, presented as text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Visual estimates from supplied footage; monitoring guidance, not a disease diagnosis.]

## Skill Version(s):

1.0.21 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
