## Description:

Detects estrus behavior in female livestock from continuous barn videos, including mounting acceptance, standing reflex, restlessness, appetite drop and vulva changes, and outputs an estrus recognition result with an optimal mating time window.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

External livestock operators and farm-management agents use this skill to analyze barn camera images or videos for female livestock estrus indicators, estrus-stage classification, historical report lookup, and a suggested mating time window. Results are intended as behavioral evidence for breeding workflows, not as standalone veterinary or reproductive-management advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Barn media, report metadata, and identifiers are sent to configured backend services for analysis and history lookup.

Mitigation: Review endpoint configuration and data-handling expectations before use, and submit only media appropriate for the configured service.

Risk: The skill silently creates or reuses a local identity and stores returned auth tokens in the workspace data area.

Mitigation: Run in a workspace where local identity and token storage are acceptable, and clear workspace data when rotating identities or decommissioning access.

Risk: Bundled development configuration references plain HTTP private-network addresses.

Mitigation: Confirm production endpoints and transport security before deployment.

Risk: Estrus recognition and mating-window output may be incomplete or unreliable when video quality, camera angle, lighting, duration, or occlusion are poor.

Mitigation: Use stable fixed-camera footage that meets the documented capture requirements and review outputs with farm procedures or qualified reproductive specialists.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-estrus-mating-behavior-detect-analysis)
- [Publisher Profile](https://clawhub.ai/user/smyx-sunjinhui)
- [Skill Demo](https://lifeemergence.com/sample.html)
- [API Documentation](references/api_doc.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands]

**Output Format:** [Markdown or JSON analysis reports, including structured behavior findings, estrus-stage labels, suggested mating time windows, report links, and optional saved result files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Historical report lookup is returned as a Markdown table; detailed analysis can be requested with basic, standard, or json detail levels.]

## Skill Version(s):

1.0.10 (source: server release metadata; artifact frontmatter states 1.0.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
