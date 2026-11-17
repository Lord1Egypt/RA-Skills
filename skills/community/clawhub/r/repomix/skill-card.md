## Description:

Pack and analyze codebases into AI-friendly single files using Repomix.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yamadashy](https://clawhub.ai/user/yamadashy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to package local directories or remote GitHub repositories into AI-friendly files, then inspect structure, patterns, token counts, and codebase findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes Repomix through mutable npm package references.

Mitigation: Pin a reviewed Repomix version or run it in a contained environment before relying on generated output.

Risk: Repository packing can include broad codebase content and may expose sensitive material in generated files.

Mitigation: Use include or ignore patterns to narrow scope, keep output in a temporary directory, and review generated files for secrets before sharing.

## Reference(s):

- [Repomix GitHub Repository](https://github.com/yamadashy/repomix)
- [Repomix ClawHub Skill Page](https://clawhub.ai/yamadashy/skills/repomix)
- [Repomix Publisher Profile](https://clawhub.ai/user/yamadashy)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and code-search examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to generate Repomix output files in a temporary directory and report repository metrics, structure, findings, and next steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
