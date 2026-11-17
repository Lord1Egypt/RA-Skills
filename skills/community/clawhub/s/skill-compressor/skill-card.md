## Description:

Compresses agent skill files to reduce token cost when a user invokes /skill-compressor or asks to optimize, compress, slim down, or debloat a skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[david0ming](https://clawhub.ai/user/david0ming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to compress bulky Claude Code skill directories while preserving operational rules. The skill writes compressed copies and a reduction report under .reduced/ so maintainers can review diffs before replacing originals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An optional unpinned npx install command may resolve changing external content over time.

Mitigation: Install through ClawHub or a reviewed and pinned source when possible.

Risk: Compressed outputs could remove behavior if the faithfulness review misses operational details.

Mitigation: Review the generated .reduced/ output with a diff and replace originals only after confirming behavior is preserved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/david0ming/skills/skill-compressor)
- [SkillReducer methodology paper](https://arxiv.org/abs/2603.29919)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown files and concise written guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes compressed copies to .reduced/ and preserves original skill files.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
