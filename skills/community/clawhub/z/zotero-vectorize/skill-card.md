## Description: <br>
Build and maintain a cross-platform local Zotero semantic index using metadata embeddings and PDF full-text chunk embeddings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yckbz](https://clawhub.ai/user/yckbz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and Zotero users use this skill to build, refresh, check, and verify local semantic indexes for Zotero bibliographic metadata and PDF full text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated vector stores, PDF text chunks, database snapshots, and path metadata can contain private Zotero library content. <br>
Mitigation: Use a private local output directory, avoid shared cloud sync unless intentional, and handle generated files as sensitive research data. <br>
Risk: The skill depends on local Python packages and embedding model downloads. <br>
Mitigation: Install dependencies in a virtual environment and review dependency installation commands before running them. <br>
Risk: Incremental updates rewrite persistent vector store files. <br>
Mitigation: Check missing Zotero items first, require user confirmation before applying updates, and keep the latest and previous backups. <br>


## Reference(s): <br>
- [Zotero Vectorize ClawHub page](https://clawhub.ai/yckbz/zotero-vectorize) <br>
- [Configuration](references/config.md) <br>
- [Data format](references/data-format.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Windows notes](references/windows.md) <br>
- [macOS notes](references/macos.md) <br>
- [Linux notes](references/linux.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON file outputs from bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local vector store files, database snapshots, retained backups, README summaries, and verification reports.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
