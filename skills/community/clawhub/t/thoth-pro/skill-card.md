## Description:

Thoth Pro helps agents generate a documentation suite for a codebase, including a README, API reference, usage guide, architecture documentation, changelog, and optional Python docstrings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scan a project and produce project documentation, API reference material, usage guidance, architecture notes, and a changelog. It can also prepare docstring content for undocumented Python symbols when configured to do so.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose broad project contents and git history in command output.

Mitigation: Review before installing on proprietary or secret-bearing repositories, avoid shared logs or remote transcripts, and run only where project contents may be disclosed.

Risk: The install step asks users to modify the system Python environment.

Mitigation: Prefer running the skill in a disposable virtual environment rather than the system Python environment.

Risk: The skill can prepare docstring changes for source files when docstring injection is enabled.

Mitigation: Set INJECT_DOCSTRINGS=no unless source edits are intended, and review generated docstrings before applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/occupythemilkyway/skills/thoth-pro)
- [ClawHub homepage metadata](https://clawhub.ai/occupythemilkyway/thoth-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documents, inline shell and Python commands, and JSON-style docstring mappings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated documentation to the configured output directory and may prepare source docstring updates when docstring injection is enabled.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
