## Description:

Display information about active processes for monitoring running programs, checking resource usage, and system diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and support engineers use this skill to inspect active local processes while monitoring systems or diagnosing resource and process-state issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Process command lines can expose sensitive strings when other programs include secrets or private data in their arguments.

Mitigation: Review process-listing output before sharing it and avoid running the skill in environments where command-line arguments may contain secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/ps-tool)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text process listings and Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local process IDs and command-line snippets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
