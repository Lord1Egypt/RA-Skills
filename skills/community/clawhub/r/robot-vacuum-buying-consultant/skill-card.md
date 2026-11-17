## Description:

Guides robot vacuum buyers through floor type, home size, pets, and navigation questions to determine the suction, mapping, filter, and automation specs they need.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arbazex](https://clawhub.ai/user/arbazex)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to evaluate robot vacuum requirements for their home before buying. It turns user answers about layout, flooring, pets, allergies, clearance, connectivity, and automation preferences into a prioritized spec recommendation and a small set of product starting points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product suggestions may become stale because model specs, regional availability, and pricing change over time.

Mitigation: Use suggestions as starting points and verify the current spec sheet, included dock/base, availability, and local pricing before buying.

Risk: Incomplete user answers can lead to unsuitable recommendations for suction, navigation, clearance, filtering, or connectivity.

Mitigation: Collect all critical home, floor, pet, allergy, furniture clearance, Wi-Fi, country, and automation details before producing the final recommendation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arbazex/skills/robot-vacuum-buying-consultant)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown consultation questions, prioritized specification lists, and numbered product suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Caps product suggestions at five and instructs users to verify current model specs, availability, and pricing locally.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
