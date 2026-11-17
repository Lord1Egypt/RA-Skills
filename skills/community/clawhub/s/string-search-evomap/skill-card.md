## Description:

High-performance string search support with adaptive strategies, multi-level pruning, and redundancy detection for large-scale text processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gatsby047-oss](https://clawhub.ai/user/gatsby047-oss)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to evaluate or adapt a C string-search benchmark for large text search, pattern matching, log analysis, and data deduplication workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shipped C implementation is unsafe for the general text-processing use cases it advertises.

Mitigation: Validate input characters, enforce bounds and allocation checks, document supported encodings, and run memory-safety tests before production use.

Risk: The advertised README usage may not match the exposed C entry points.

Mitigation: Confirm the public API and compile path before integrating the code into an application or agent workflow.

Risk: Security evidence marks the release as suspicious even though no hidden network, credential, persistence, or privilege behavior was reported.

Mitigation: Review the code before installing or reusing it in production and apply the security guidance from the ClawHub scan.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gatsby047-oss/skills/string-search-evomap)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [code, shell commands, guidance]

**Output Format:** [Markdown with inline C and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes C benchmark code and usage guidance; review generated or reused code before execution.]

## Skill Version(s):

1.0.0 (source: server release and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
