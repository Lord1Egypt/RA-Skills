## Description:

Analyzes video from a pet toilet or designated area to report suspected defecation events and issue a cleaning trigger after the pet leaves; a separate smart-home integration is needed to operate a vacuum.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners and smart-home integrators can use it to analyze camera video from a designated pet toilet, record suspected defecation events, and pass a trigger to a separately configured cleaning system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence marks the release suspicious due to reported credential handling, account and profile persistence, and capabilities unrelated to its stated purpose. The scan is incomplete and the external upload behavior is unclear.

Mitigation: Avoid installation until the publisher explains these capabilities and the upload path; verify the explanation and complete a security review before providing credentials or pet video.

## Reference(s):

- [API reference](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub skill listing](https://clawhub.ai/smyx-sunjinhui/skills/smyx-poop-clean-trigger-analysis)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Event signal]

**Output Format:** [Structured analysis results and event status in JSON or text; report lists can be presented as Markdown tables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Vision-based event detection only; it does not provide medical diagnosis or directly operate a vacuum.]

## Skill Version(s):

1.0.15 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
