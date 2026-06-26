## Description: <br>
Indexes and searches local project files by monitoring file changes, storing searchable metadata, and returning keyword results, intent-based recommendations, and file statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zgbin](https://clawhub.ai/user/zgbin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to locate code files, scripts, configuration, and documentation in local workspaces through keyword search, intent matching, recent-file views, type filters, and index statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local indexing can store file paths and short content snippets from broad workspace locations. <br>
Mitigation: Narrow watched directories, exclude secrets and private projects, and confirm where file_index.db is stored before enabling monitoring. <br>
Risk: Automatic watchers and broad triggers can index more files than a user intended. <br>
Mitigation: Start with manual scans or a limited watch scope, then expand only after reviewing the indexed paths and trigger behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zgbin/zgbin-file-indexer) <br>
- [README](README.md) <br>
- [Install guide](INSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with command examples and JSON-formatted command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include local file paths, file types, short content summaries, tags, timestamps, deletion status, and aggregate statistics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
