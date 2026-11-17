## Description:

Generate block randomization lists for RCTs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical trial designers, preclinical study teams, and supporting developers use this skill to generate block randomization schedules for RCT or animal study allocation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can overwrite arbitrary writable files through its output path.

Mitigation: Run it in a sandbox or controlled workspace, choose an output path inside the project, and check for existing files before execution.

Risk: The skill makes an unsupported clinical allocation-concealment claim.

Mitigation: Do not rely on it for regulated or high-stakes clinical allocation concealment without a validated randomization process and appropriate access controls.

## Reference(s):

- [Randomization Gen on ClawHub](https://clawhub.ai/aipoch-ai/skills/randomization-gen)

## Skill Output:

**Output Type(s):** [text, files, shell commands, configuration]

**Output Format:** [CSV file with console text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the full randomization schedule to the configured output path and prints a short allocation preview.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
