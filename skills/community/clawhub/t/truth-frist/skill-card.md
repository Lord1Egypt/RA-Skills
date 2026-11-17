## Description:

Evidence-first verification for status, config, file contents, actions, connectivity, mounts, and model selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[royhk920](https://clawhub.ai/user/royhk920)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to make agents verify claims about runtime status, configuration, files, connectivity, mounts, actions, and model selection before answering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verification requests may lead the agent to inspect local configuration, log, or environment files.

Mitigation: Keep verification requests focused, avoid unnecessary sensitive paths, and review proposed commands before running checks that may expose secrets or private data.

Risk: When direct evidence is unavailable, the agent may only be able to classify a claim as Inferred or Unknown.

Mitigation: Use the skill's next-step commands to gather primary evidence before relying on the result for operational decisions.

## Reference(s):

- [Patterns](references/patterns.md)
- [ClawHub skill page](https://clawhub.ai/royhk920/skills/truth-frist)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with evidence classifications, citations, and inline shell commands when follow-up checks are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Classifies claims as Verified, Inferred, or Unknown and provides next-step commands for Unknown claims.]

## Skill Version(s):

1.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
