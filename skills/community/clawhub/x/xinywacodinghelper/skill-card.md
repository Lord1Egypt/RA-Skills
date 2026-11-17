## Description:

Guides agents through safe, minimal, production-quality code changes in existing repositories using staged understanding, planning, implementation, validation, review, and recovery practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xinyue-wang](https://clawhub.ai/user/xinyue-wang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill for complex code changes in large existing repositories where repo access checks, incremental understanding, minimal edits, tests, and visible progress are required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow retains local repository indexes and run logs under /home/vibe/aksclaw-data.

Mitigation: Use it only where retaining local metadata is acceptable, and review or clean those files according to local data-handling requirements.

Risk: The skill is intended for complex repository changes and can be inappropriate for simple code tasks.

Mitigation: Apply the routing rule before use and reserve the workflow for multi-file, debugging, or production-safe code changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xinyue-wang/skills/xinywacodinghelper)
- [Publisher profile](https://clawhub.ai/user/xinyue-wang)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured progress, error, recovery, confidence, and final output sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local index and run-log files under /home/vibe/aksclaw-data when followed by an agent.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
