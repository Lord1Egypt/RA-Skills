## Description:

Analyzes aquarium video to identify fish flashing and scraping, count these events, and flag possible ectoparasite risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Aquarists, aquarium staff, and aquaculture operators can review fixed-camera footage for repeated fish rubbing behavior and receive a structured risk report. Use the result as a prompt to observe the fish and seek qualified veterinary advice, not as a diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags account, credential, remote-service, privacy, and execution-control concerns.

Mitigation: Review remote-service and credential handling before installation; avoid sending private footage or identity data until the service's handling is understood, and limit access to what is needed.

Risk: Video behavior can suggest a health concern but cannot confirm a parasite or determine treatment.

Mitigation: Use alerts as prompts for observation and ask a qualified aquatic veterinarian to confirm any diagnosis and treatment.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release](https://clawhub.ai/18072937735/skills/smyx-fish-flashing-scraping-detection-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured JSON analysis report; Markdown table for historical report listings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports flashing and scraping counts, risk level, suggested next steps, and report links. Behavior-based alerts do not confirm disease.]

## Skill Version(s):

1.0.18 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
