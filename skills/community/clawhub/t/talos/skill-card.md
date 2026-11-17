## Description:

Talos plans and batches a 4-week social media content calendar with platform-specific captions, posting-time guidance, content pillar rotation, and JSON and Markdown exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing teams use this skill to generate a local 4-week posting plan for Twitter/X, LinkedIn, Instagram, and Threads from a brand topic, posting cadence, content pillars, and tone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command modifies system Python packages and installs an unpinned dependency.

Mitigation: Install dependencies in an isolated virtual environment and pin or review the dependency before use.

Risk: Generated calendar files are written to the current working directory and may overwrite existing files with the same generated names.

Mitigation: Run the skill in a dedicated working directory where replacing generated calendar files is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/occupythemilkyway/skills/talos)
- [ClawHub metadata homepage](https://clawhub.ai/occupythemilkyway/talos)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown instructions with inline bash and Python code; generated runtime artifacts are JSON and Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated calendar is written locally as social_calendar_<topic>_<date>.json and social_calendar_<topic>_<date>.md.]

## Skill Version(s):

1.0.4 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
