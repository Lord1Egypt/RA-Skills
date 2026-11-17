## Description:

Using a fixed kitchen camera that captures the stove area, this skill analyzes kitchen video or images to detect human activity and stove flame or heat-source status, then reports possible unattended stove-left-on alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

External users, caregivers, smart-home operators, and care-facility staff can use this skill to analyze fixed kitchen-camera footage for unattended stove use and receive structured kitchen-safety monitoring results. It is intended as an auxiliary monitoring workflow for elder-care and kitchen-safety scenarios, with human confirmation expected for urgent alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kitchen camera footage, video URLs, and identifiers may be processed by remote services.

Mitigation: Confirm consent, backend endpoints, report retention, and data-handling controls before using the skill in homes or care settings.

Risk: The skill can create or reuse persistent local identity and token state.

Mitigation: Review token storage and identity lifecycle expectations before installation or deployment.

Risk: Gas-valve automation or urgent alerts can affect physical safety workflows.

Mitigation: Require human confirmation and validate automation controls before enabling any valve shutdown or emergency-response integration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-kitchen-stove-left-on-detection-analysis)
- [Kitchen Stove Left-On Detection API Reference](references/api_doc.md)
- [Shared Analysis API Reference](skills/smyx_analysis/references/api_doc.md)
- [Skill Demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and JSON-compatible structured analysis text, including detection results, alert level, recommendations, and report links when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query remote analysis services and may write analysis output to a user-specified file.]

## Skill Version(s):

1.0.9 (source: server release metadata; artifact frontmatter reports 1.0.12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
