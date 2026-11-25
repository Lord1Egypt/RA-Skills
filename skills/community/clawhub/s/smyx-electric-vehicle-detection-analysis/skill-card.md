## Description:

Detects electric motorcycles and e-bikes in restricted areas from images and video, counts apparent parking and driving violations, and produces alerts and management suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Safety and facilities teams in parks, communities, campuses, and organizations use the skill to review images or video for electric vehicle activity in restricted areas and support follow-up. Its reports are for management reference and should be checked by a person before treating a violation as confirmed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports remote account, credential, and media handling, including authenticated requests to caller-supplied URLs.

Mitigation: Review the service and request destinations before use; avoid sensitive media and install only if you need the described behavior and accept its data handling.

Risk: The scan rates the skill suspicious because some reported behavior does not consistently match its stated detection purpose; the scan is incomplete because one reference was unresolved.

Mitigation: Review the skill and unresolved reference before execution. Treat the scan as a reason for caution, not proof of malicious intent or that the behaviors have been invoked.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill introduction](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-electric-vehicle-detection-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [JSON or Markdown report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can include detection counts, violation levels, warnings, and management suggestions; output can optionally be saved to a file.]

## Skill Version(s):

9.9.23 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
