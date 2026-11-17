## Description:

Generates structured survey questionnaires from a user's research goal and renders them as local HTML forms that can be opened, answered, copied, printed, or exported.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenobiazizi](https://clawhub.ai/user/zenobiazizi)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to turn a short survey objective into a practical questionnaire for customer satisfaction, NPS, product research, event feedback, internal surveys, or training evaluation. It supports preview and internal review through a generated local HTML form, with question-copying for deployment through a survey platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Survey goals are sent to Dify for generation.

Mitigation: Tell users before use and limit submitted text to the minimum survey goal, audience, and decision context needed.

Risk: The distributed package contains a reusable service token.

Mitigation: Revoke the exposed token and move service credentials to protected runtime storage before deployment.

Risk: Generated HTML uses unsafe raw template insertion that could run injected browser code.

Mitigation: Safely encode embedded survey data before opening generated forms or asking users to enter sensitive responses.

## Reference(s):

- [Survey Form Generator on ClawHub](https://clawhub.ai/zenobiazizi/skills/survey-form-generator)
- [Dify API endpoint used by the skill](https://api.dify.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, shell commands]

**Output Format:** [Markdown guidance with generated JSON-backed HTML form files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local HTML survey forms and a copyable question list; generated forms do not collect multi-user responses by themselves.]

## Skill Version(s):

1.0.1 (source: server evidence and CHANGELOG, released 2026-08-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
