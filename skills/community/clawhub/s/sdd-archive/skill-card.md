## Description:

Archives completed feature specs into a project's global knowledge base by extracting key decisions, updating constraints and domain indexes, and moving the feature directory into spec/archive/.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mahingbun-dev](https://clawhub.ai/user/mahingbun-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to archive completed specification-driven development feature directories into global project documentation while preserving domain summaries, constraints, indexes, and archive location.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom feature path can reach a Bash move operation without clear validation.

Mitigation: Use only trusted feature directories and avoid the custom path option unless the path is clearly confined to spec/feature_*.

Risk: The workflow can perform broad documentation and archive changes without one final consolidated confirmation.

Mitigation: Ask the agent to show a complete change plan before it writes files, generates images, deletes or merges domain docs, or moves the feature directory.

Risk: Running the archive workflow in repositories with sensitive code or important spec files may expose or alter material project context.

Mitigation: Review the skill before installing and run it only on repositories and feature directories you trust.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mahingbun-dev/skills/sdd-archive)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation updates, concise status messages, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Chinese user-facing archive summaries and may request user confirmation before broad file updates.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
