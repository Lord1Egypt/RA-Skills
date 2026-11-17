## Description:

Basic clothing repair and maintenance skills. Use when someone needs to fix torn clothing, replace a button, hem pants, patch holes, or wants to stop wasting money replacing fixable clothes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to get practical guidance for common clothing repairs and maintenance tasks, including replacing buttons, fixing split seams, patching holes, hemming garments, addressing zipper issues, removing stains, ironing, and hand-washing delicates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests filesystem access even though the release evidence describes it as mostly instructional.

Mitigation: Review the permission request before installation and remove filesystem access unless a concrete file operation is required.

Risk: The skill includes an ongoing location-based seasonal reminder without clear opt-in.

Mitigation: Require explicit user consent before scheduling reminders, provide a clear cancellation path, and keep location-based suggestions user-directed.

## Reference(s):

- [Singer Sewing Reference Guides](https://www.singer.com/sewing-resources)
- [ASTM International Textile Care Standards](https://www.astm.org)
- [Consumer Reports Clothing Longevity Studies](https://www.consumerreports.org)
- [Anthropic Labor Market Impacts of AI](https://www.anthropic.com/research/labor-market-impacts)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with checklists and step-by-step repair instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include localized terminology, measurements, cost estimates, and user-directed store suggestions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
