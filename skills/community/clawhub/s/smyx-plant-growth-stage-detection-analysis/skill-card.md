## Description:

Analyzes plant images or videos to identify visible growth stages and phenological features, returning a confidence-rated structured report and general care guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Growers and operators of smart pots, home grow systems, greenhouses, and plant factories use the skill to assess plant images or videos for developmental stage, visible phenological cues, and confidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence flags automatic service-account registration and credential-handling concerns, including separation of secrets from account identifiers and protected token storage.

Mitigation: Review account onboarding explicitly, keep credentials separate from account identifiers, and protect stored tokens.

Risk: Media processing uses an external service and may incur charges; the security guidance says export-only mode is not confirmed working.

Mitigation: Submit only media approved for external processing, check applicable costs, and verify export-only mode before relying on it.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-plant-growth-stage-detection-analysis)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured JSON analysis report text with a report link; history listings are JSON text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include an estimated growth stage, visible cues, and confidence; detail can be basic, standard, or JSON.]

## Skill Version(s):

1.0.11 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
