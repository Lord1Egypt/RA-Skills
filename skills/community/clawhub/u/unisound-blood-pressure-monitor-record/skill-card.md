## Description:

Records patient blood pressure measurements for chronic disease management, producing structured JSON and patient-facing Markdown guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and chronic-care workflows use this skill to capture systolic pressure, diastolic pressure, heart rate, measurement time, and notes from supported input files. The skill returns structured blood-pressure records and concise Markdown guidance without replacing clinical judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Blood-pressure records and notes may contain sensitive health information and are sent to an external medical model.

Mitigation: Use the skill only when users understand this data flow, avoid identifiers in notes, and provide only the minimum necessary health data.

Risk: Broad document and image parsing increases exposure to malformed or untrusted input files.

Mitigation: Prefer JSON or CSV input when possible and avoid untrusted documents or images.

Risk: The skill accepts the model app key through a command-line argument.

Mitigation: Use a safer secret mechanism than command-line app keys when the host platform provides one.

## Reference(s):

- [HealthLog](https://healthlog.dev/)
- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-blood-pressure-monitor-record)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [UTF-8 JSON with structured data and a Markdown text field]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided app key for the external medical model; supports JSON, CSV, Excel, text, Markdown, PDF, Word, and image inputs.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
