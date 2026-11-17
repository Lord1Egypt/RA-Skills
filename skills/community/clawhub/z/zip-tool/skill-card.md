## Description:

Provides a small local helper for creating ZIP archives from specified files; its documentation also claims broader archive-management features that the bundled script does not implement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents can use this skill when they need to package selected local files into a ZIP archive. Review claimed archive-management options before relying on them because release security evidence says the included implementation is a small ZIP creation helper, not a full archive manager.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release documentation substantially overstates the included script's capabilities.

Mitigation: Validate archive behavior against the bundled script before relying on extraction, listing, deletion, update, recursion, compression-level, password, or JSON features.

Risk: Password examples in the documentation may encourage exposing secrets on the command line.

Mitigation: Avoid command-line password examples and use reviewed secret-handling practices before adding password-protected archive workflows.

Risk: Archive operations can overwrite or package unintended local files if paths are not reviewed.

Mitigation: Review requested file paths and archive destinations before execution, especially when operating in shared or sensitive directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/zip-tool)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown with inline shell commands and code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local ZIP archive creation commands or invoke the bundled Python helper.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
