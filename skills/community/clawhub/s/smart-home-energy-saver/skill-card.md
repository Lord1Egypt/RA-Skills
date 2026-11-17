## Description:

Analyze home energy usage and propose safe, read-only automation plans for savings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codedao12](https://clawhub.ai/user/codedao12)

### License/Terms of Use:


## Use Case:

External users and home automation developers use this skill to analyze Home Assistant energy and device data, identify savings opportunities, and prepare draft automation YAML for manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated automation YAML could be enabled without adequate review and change device schedules in ways that affect comfort, safety, or accessibility.

Mitigation: Manually review every draft automation, exclude medical devices, security systems, and critical appliances, and roll out changes through Home Assistant only after user approval.

Risk: Home Assistant tokens, home addresses, or device identifiers could expose sensitive household information if shared unnecessarily.

Mitigation: Use read-only Home Assistant tokens or exported data, keep tokens out of plain text files, and avoid including home addresses or unnecessary device identifiers in prompts or outputs.

## Reference(s):

- [Auth](references/auth.md)
- [Endpoints](references/endpoints.md)
- [Overview](references/overview.md)
- [Safety](references/safety.md)
- [Troubleshooting](references/troubleshooting.md)
- [UX](references/ux.md)
- [Webhooks](references/webhooks.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with YAML code blocks and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only recommendations; generated automations are drafts for manual review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
