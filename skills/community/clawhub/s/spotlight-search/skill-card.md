## Description: <br>
Search files, apps, and metadata on macOS using Spotlight CLI tools (`mdfind`, `mdls`, `mdutil`) with a fallback script for cases where indexing is incomplete. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mozi1924](https://clawhub.ai/user/mozi1924) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and macOS users use this skill to find files, applications, and metadata on a Mac through Spotlight CLI tools, with a fallback path-based search when indexing is incomplete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searches can expose local file paths or file metadata in the agent chat. <br>
Mitigation: Prefer folder-scoped searches for sensitive areas and review results before sharing or acting on them. <br>
Risk: Spotlight reindexing with `sudo mdutil -E /` is privileged and system-wide. <br>
Mitigation: Use `mdutil` mainly for status checks and approve reindexing only when intentionally rebuilding Spotlight. <br>
Risk: Spotlight results can be incomplete when indexing is stale or a directory is excluded. <br>
Mitigation: Use scoped `mdfind` queries first, then the bundled fallback script for filename or path matching when a known file is missing. <br>


## Reference(s): <br>
- [mdfind Query Reference](references/mdfind-queries.md) <br>
- [Apple Uniform Type Identifiers Reference](https://developer.apple.com/documentation/uniformtypeidentifiers) <br>
- [ClawHub Skill Page](https://clawhub.ai/mozi1924/spotlight-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local file paths and metadata; no API calls or credential variables are required.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
