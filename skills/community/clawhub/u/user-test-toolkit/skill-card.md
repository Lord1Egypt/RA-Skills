## Description:

User Test Toolkit helps agents add browser-side usability tracking and embedded survey flows for product testing, user research, event collection, and A/B evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ildar981105-create](https://clawhub.ai/user/ildar981105-create)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to instrument web applications with user behavior tracking, milestone capture, task guidance, checkpoint surveys, SUS, EV, NPS, and SAM feedback collection during usability studies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The toolkit can collect and transmit detailed user behavior data.

Mitigation: Use it only where participants have clear notice and consent, and restrict deployment to test environments or controlled studies.

Risk: Collected events may include URLs, referrers, filenames, or free-text responses.

Mitigation: Configure a trusted HTTPS endpoint, redact sensitive fields before storage, and avoid collecting free-text unless it is needed.

Risk: Survey rendering may be unsafe with tenant- or user-controlled survey configuration.

Mitigation: Fix unsafe innerHTML rendering or sanitize all survey configuration before using untrusted inputs.

## Reference(s):

- [Tracker API Reference](references/tracker-spec.md)
- [Survey Configuration Reference](references/survey-spec.md)

## Skill Output:

**Output Type(s):** [Code, Configuration, Guidance, Markdown]

**Output Format:** [Markdown guidance with HTML and JavaScript snippets plus browser-side JavaScript assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes configurable tracker and survey assets that send collected events to a deployment-provided endpoint.]

## Skill Version(s):

4.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
