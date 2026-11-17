## Description:

Generates random maps and equipment loadouts for 三角洲行动 gameplay challenges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fushisanlang](https://clawhub.ai/user/fushisanlang)

### License/Terms of Use:

MIT-0

## Use Case:

External players, streamers, and challenge hosts use this skill to generate randomized 三角洲行动 map and equipment combinations for entertainment, livestream interaction, and casual challenge modes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each run contacts a custom third-party web service.

Mitigation: Review the third-party service dependency before installation and run the skill only where sharing connection metadata with that service is acceptable.

Risk: Randomizer content can change if the service changes or is compromised.

Mitigation: Treat generated loadouts as entertainment guidance and review results before using them in hosted or public challenge contexts.

Risk: Network calls may hang because no timeout is documented in the security evidence.

Mitigation: Run the skill in an environment where stalled requests can be interrupted or supervised.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fushisanlang/skills/sanjiaozhou-random)
- [Publisher profile](https://clawhub.ai/user/fushisanlang)
- [Map randomizer API](https://sanjiaozhou.fushisanlang.cn/api/random_map_status)
- [Equipment randomizer API](https://sanjiaozhou.fushisanlang.cn/api/random_arm_equipment)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON object containing a status flag and generated result text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs without user parameters and returns either generated game randomizer text or an error message.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
