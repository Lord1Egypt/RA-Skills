## Description:

Analyzes adult facial images or short videos to estimate a fatigue/stress index and return a structured feature report with directional suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and workplace wellness teams can use adult facial images or short videos to get a facial-feature-based fatigue/stress score, feature summary, and directional suggestions. The result is an informational status indicator, not a medical diagnosis or clinical stress assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags privacy and consent concerns around remote processing of facial media.

Mitigation: Obtain the subject's consent before submitting facial media, and review how images and reports are handled and protected.

Risk: Registration and identity/token handling are flagged for review.

Mitigation: Review the service's identity and token handling before installation and use.

Risk: The security summary raises concern that analysis may run despite an export-only option.

Mitigation: Treat the export-only behavior as unverified; avoid using sensitive media until the behavior is confirmed.

Risk: The security scan is partial because it could not resolve a local path-like reference, so its evidence is incomplete.

Mitigation: Review the unresolved reference and the package before use.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill introduction](https://lifeemergence.com/sample.html)
- [ClawHub skill listing](https://clawhub.ai/smyx-sunjinhui/skills/smyx-adult-facial-fatigue-stress-index-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance, Markdown]

**Output Format:** [Structured analysis report (JSON or text); history results as a Markdown table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a fatigue/stress score from 0 to 100, feature metrics, a level, and directional suggestions; it is not a medical diagnosis or clinical stress assessment.]

## Skill Version(s):

1.0.14 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
