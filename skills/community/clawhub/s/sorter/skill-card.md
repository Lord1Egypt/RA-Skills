## Description:

Sorting algorithm and system reference for comparison sorts, distribution sorts, parallel sorting, and industrial sortation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and operations practitioners use this skill to choose sorting strategies, compare algorithmic complexity, and reason about warehouse or postal sortation systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may rely on static sorting guidance for production algorithm or sortation design choices without validating workload-specific constraints.

Mitigation: Review recommendations against the target data shape, throughput requirements, memory budget, and operational constraints before deployment.

Risk: The skill exposes commands that run a local shell script.

Mitigation: Run only the documented commands; the security evidence reports that the inspected script prints static guidance and does not access files, credentials, or networks.

## Reference(s):

- [BytesAgain homepage](https://bytesagain.com)
- [ClawHub skill listing](https://clawhub.ai/ckchzh/skills/sorter)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and terminal text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces static sorting reference guidance; no API calls, credential access, or network access are reported by security evidence.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
