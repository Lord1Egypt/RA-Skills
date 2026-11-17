## Description:

Search files, apps, and metadata on macOS using Spotlight CLI tools (`mdfind`, `mdls`, `mdutil`) and a fallback script when indexing is incomplete.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mozi1924](https://clawhub.ai/user/mozi1924)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and macOS users use this skill to construct Spotlight searches, inspect file metadata, and fall back to local filename or path matching when Spotlight indexing is incomplete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can search local Spotlight-indexed content, which may include sensitive filenames, paths, metadata, or document contents.

Mitigation: Use explicit directory scoping such as `mdfind -onlyin` when possible, and review proposed searches before execution.

Risk: The security summary reports a directory-scoping bug in the bundled fallback behavior.

Mitigation: Prefer explicit `-onlyin` scoping for Spotlight searches and avoid relying on the bundled script for home-directory-limited searches until the issue is fixed.

Risk: The skill includes guidance for `sudo mdutil -E /`, a privileged system-wide Spotlight reindex command.

Mitigation: Do not approve system-wide reindexing unless the user intentionally requests that system-level change.

## Reference(s):

- [mdfind Query Reference](references/mdfind-queries.md)
- [Apple Uniform Type Identifiers](https://developer.apple.com/documentation/uniformtypeidentifiers)
- [ClawHub Spotlight Search Skill Page](https://clawhub.ai/mozi1924/skills/spotlight-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces macOS-specific search and metadata inspection guidance; commands may access local Spotlight-indexed content.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
