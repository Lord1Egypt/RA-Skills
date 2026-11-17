## Description:

Generates multiple-choice quizzes from document content and returns a quiz link and QR code for participants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alsxie](https://clawhub.ai/user/alsxie)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, trainers, and teams use this skill to turn course or reference documents into multiple-choice quizzes, publish a quiz URL or QR code, and collect answer submissions with basic score statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document content and quiz data may be transmitted to configured cloud services or exposed through the web app.

Mitigation: Use only documents approved for those services, require authentication before exposing the app, and review data retention expectations before deployment.

Risk: API keys and deployment controls are under-scoped by default.

Mitigation: Store ARK_API_KEY in a managed secret mechanism, avoid running the service as root, and replace runtime package installs with pinned setup steps.

Risk: TLS verification is disabled for the quiz creation helper.

Mitigation: Remove the TLS bypass and use a certificate-validated endpoint before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alsxie/skills/quiz-maker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-producing helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include a quiz URL, QR code image path, generated question JSON, and operational status messages.]

## Skill Version(s):

1.4.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
