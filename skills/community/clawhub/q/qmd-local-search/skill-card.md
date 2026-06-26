## Description: <br>
Fast local search for markdown files, notes, and docs using qmd CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bheemreddy181](https://clawhub.ai/user/bheemreddy181) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and other agent users use this skill to search indexed local markdown, notes, documentation, and code-adjacent files with qmd CLI commands. It supports file discovery, keyword search, semantic search, reranked search, and targeted retrieval of file contents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Indexing broad local directories may expose sensitive files in search or retrieval results. <br>
Mitigation: Use named collections scoped to intended directories and avoid indexing sensitive paths unless that access is deliberate. <br>
Risk: Retrieving full files or large globs can return more local content than needed. <br>
Mitigation: Prefer line limits, byte limits, and targeted paths when using qmd get or multi-get. <br>
Risk: The skill depends on the local qmd CLI and its model download source. <br>
Mitigation: Install only in environments where the qmd CLI and model source are already trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bheemreddy181/qmd-local-search) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may return file paths, snippets, full document content, line-numbered content, or JSON when qmd flags request those formats.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
