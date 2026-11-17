## Description:

Analyze, syntax-check, reindent, and distribute Swift source code with the SwiftButler CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odrobnik](https://clawhub.ai/user/odrobnik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when working with Swift files or packages to inspect API shape, run fast syntax checks, normalize indentation, or split large Swift source files into smaller declaration-based files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recursive reindent or distribute commands can rewrite or create Swift source files by design.

Mitigation: Run dry-run where available before applying changes and review version-control diffs afterward.

Risk: Command guidance may be applied to the wrong Swift paths or visibility scope.

Mitigation: Confirm target paths, selected SwiftButler subcommand, and output format before executing commands.

## Reference(s):

- [SwiftButler project homepage](https://github.com/Cocoanetics/SwiftButler)
- [ClawHub SwiftButler skill page](https://clawhub.ai/odrobnik/skills/swiftbutler)
- [Publisher profile](https://clawhub.ai/user/odrobnik)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash command examples and concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide commands that inspect, validate, rewrite, or create Swift source files through the SwiftButler CLI.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
