## Description:

Split files into smaller pieces by size, line count, or number of chunks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to break large logs, binary data, or text files into smaller parts for transfer, inspection, or downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The splitter can silently overwrite predictable output files that already match the selected prefix.

Mitigation: Run it in a dedicated output directory, choose a non-conflicting prefix, and review generated paths before relying on the output.

Risk: The documentation describes an -n chunk-count option and line-based splitting behavior that the artifact does not fully implement.

Mitigation: Validate the supported command-line options before use and prefer the implemented byte-size or prefix controls until the publisher updates the script or documentation.

Risk: The security verdict is suspicious because the skill is purpose-aligned but has overwrite and documentation accuracy issues.

Mitigation: Review before installing, avoid elevated privileges, and scan or test the skill in a controlled workspace before broader use.

## Reference(s):

- [Split Tool ClawHub page](https://clawhub.ai/dinghaibin/skills/split-tool)

## Skill Output:

**Output Type(s):** [text, shell commands, code, guidance]

**Output Format:** [Markdown with command examples and generated file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces smaller output files on disk using a caller-selected prefix.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
