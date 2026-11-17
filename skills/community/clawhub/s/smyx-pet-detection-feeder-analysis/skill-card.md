## Description:

Based on computer vision, automatically detects and recognizes cats and dogs appearing in the target area from the perspective of feeder/IPC cameras, and supports pet identity recognition and database entry, suitable for pet identification management in smart feeding scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

People operating smart feeders or fixed-view IPC cameras use the skill to detect cats and dogs in images or videos, identify and enroll individual pets, and review historical analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local media may be processed remotely.

Mitigation: Confirm where media is sent and how it is retained before use; submit only media approved for that service.

Risk: The security review reports possible account creation and credential handling.

Mitigation: Review the account and authentication behavior before installation, and avoid supplying credentials until their handling is understood.

Risk: The security review reports unexpected remote and file-system side effects and behavior that may exceed the described pet-identification purpose.

Mitigation: Review the operations and access requested, and limit use to the intended task until the reported behavior is understood.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-pet-detection-feeder-analysis)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Guidance]

**Output Format:** [Text or JSON analysis reports; Markdown tables for historical reports, with report links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes pet detection and identification results, enrollment results, recommendations, and historical report links when available.]

## Skill Version(s):

1.0.18 (source: server-resolved release metadata; artifact frontmatter lists 1.0.26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
