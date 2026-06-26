## Description: <br>
Sandwich is advertised for blockchain sandwich-operation analysis, but server security review identifies the artifact as a local data-entry CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this release as a simple local CLI for adding, listing, searching, removing, and exporting text entries. It should not be relied on as blockchain sandwich-analysis tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is advertised as blockchain sandwich analysis, but the server security review identifies the included script as a local note database. <br>
Mitigation: Install only when the intended use is simple local text entry, listing, search, deletion, and export. <br>
Risk: Added content is stored unencrypted under ~/.sandwich by default and exports are written as plaintext files in the current directory. <br>
Mitigation: Do not enter secrets, wallet data, private research, or incident details; configure SANDWICH_DIR to an appropriate local path and review exported files before sharing. <br>
Risk: The remove command can delete entries without confirmation. <br>
Mitigation: Review entry numbers before deleting and keep backups of data that must be retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/sandwich) <br>
- [Publisher profile](https://clawhub.ai/user/ckchzh) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text CLI output and Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local JSONL data under the configured SANDWICH_DIR and can export plaintext JSON or CSV files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
