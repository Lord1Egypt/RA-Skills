## Description:

Automatically detects electric motorcycles and e-bikes in restricted areas based on computer vision. It supports real-time detection for both video streams and images, counts the number of illegal parking or driving instances, and triggers violation alerts to assist with safety management in parks, communities, and organizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Safety teams in parks, communities, campuses, and other managed areas use the skill to analyze surveillance images or video for electric two-wheelers in restricted zones and receive counts, violation alerts, and management suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The supplied security assessment rates the skill suspicious due to credential and account handling, behavior beyond its stated vehicle-detection purpose, media uploads, and possible unintended analysis; scanner coverage is incomplete.

Mitigation: Before installing, verify the account and credential handling, where credentials and video are sent, and whether history retrieval and persistent user records are necessary for your use.

Risk: Detection results may be inaccurate or misleading for enforcement decisions.

Mitigation: Treat results as decision support and have a person review the footage before confirming a violation.

Risk: Video and image analysis can involve personal information.

Mitigation: Use media only when authorized and follow applicable privacy requirements.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill introduction](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured detection reports and Markdown report lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can include detected vehicle counts, violation levels, alerts, and management suggestions; report lists are formatted as Markdown tables.]

## Skill Version(s):

9.9.22 (source: server-resolved ClawHub release metadata; artifact frontmatter lists 1.0.26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
