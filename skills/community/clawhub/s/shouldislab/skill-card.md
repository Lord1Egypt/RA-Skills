## Description:

shouldislab helps an agent evaluate Pokemon TCG card grading decisions by identifying the card, comparing raw and graded market values, estimating grading ROI, and returning a slab-or-skip verdict.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kewang0622](https://clawhub.ai/user/kewang0622)

### License/Terms of Use:

MIT-0

## Use Case:

External collectors and agent users use this skill to decide whether a Pokemon TCG card is worth professional grading. It supports card identification, current market price comparison, grading-cost estimates, ROI scenarios for likely grades, and a concise SLAB IT, SKIP IT, or MAYBE recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Current card prices, grading fees, turnaround times, and sold-listing availability can change, making ROI estimates stale or incomplete.

Mitigation: Use current lookups across multiple market sources, state when sold-price data is unavailable, and present ROI as an estimate rather than financial certainty.

Risk: Installing from an unpinned remote main-branch command may fetch content that differs from the reviewed package.

Mitigation: Install from the reviewed packaged SKILL.md or a pinned, verified release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kewang0622/skills/shouldislab)
- [Packaged skill instructions](artifact/SKILL.md)
- [Packaged README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with ROI tables, source notes, caveats, and a concise verdict.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs estimates based on current card-market and grading-cost lookups; results should not be treated as financial certainty.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
