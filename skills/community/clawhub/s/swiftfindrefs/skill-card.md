## Description:

Use swiftfindrefs (IndexStoreDB) to list every Swift source file referencing a symbol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelversus](https://clawhub.ai/user/michaelversus)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill during Swift refactors to find source files that reference a symbol, constrain edits for missing imports, and audit usage before renaming or deleting APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation uses a third-party Homebrew tap that is not pinned to a specific repository revision.

Mitigation: Verify trust in the tap before installation and pin or audit the exact repository revision in managed environments.

Risk: The tool reads Xcode indexing data and returns absolute source file paths from Swift projects.

Mitigation: Run it only in intended project workspaces and review returned paths before using them to scope edits.

## Reference(s):

- [CLI reference](references/cli.md)
- [Workflows](references/workflows.md)
- [Troubleshooting](references/troubleshooting.md)
- [SwiftFindRefs Homebrew tap](https://github.com/michaelversus/SwiftFindRefs.git)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Code]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to use absolute Swift source file paths returned by swiftfindrefs as the edit scope.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
