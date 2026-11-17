## Description:

Detects baby cries via audio AI in real time, analyzes likely causes, and identifies needs such as hunger, tiredness, pain, discomfort, or irritability to assist caregivers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

External caregivers and agent operators use this skill to submit infant cry audio or video for structured analysis of likely needs and to query cloud-hosted historical analysis reports. The results are parenting-support guidance and should not replace medical evaluation for persistent crying or distress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive baby media may be sent through broad cloud network code beyond the narrow audio-only description.

Mitigation: Install only after the publisher narrows the skill to disclosed media types and documents the cloud data flow clearly.

Risk: The skill silently links user identity and may create or reuse an account without explicit user consent.

Mitigation: Require explicit consent and clear disclosure before account creation, identity linking, or historical report lookup.

Risk: Cloud tokens may be stored persistently.

Mitigation: Protect token storage with appropriate local controls or avoid persistent token storage before deployment.

Risk: Non-production or non-HTTPS endpoints may be present in configuration.

Mitigation: Use HTTPS production endpoints only and remove development endpoint configurations from release packages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-infant-cry-analysis)
- [Publisher profile](https://clawhub.ai/user/smyx-sunjinhui)
- [Skill demo](https://lifeemergence.com/sample.html)
- [API documentation](artifact/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown or JSON analysis text, with optional file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include structured recognition results, risk prompts, suggestions, historical report lists, and report export links.]

## Skill Version(s):

1.0.11 (source: server release metadata; artifact frontmatter says 1.0.15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
