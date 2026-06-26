## Description: <br>
Thesaurus provides a local command-line history tracker for text entries with search, statistics, recent activity, and export features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to record local command-line text entries, inspect activity and statistics, search saved history, and export logs. It should not be relied on as a functional synonym or antonym lookup tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Capability mismatch: security evidence says the release is labeled as a thesaurus but behaves like a local text-history tracker and does not implement real synonym or antonym lookup. <br>
Mitigation: Use it only for local history, search, statistics, and export workflows; verify lexical alternatives with a separate trusted source. <br>
Risk: Text retention: entered text may be retained locally under ~/.local/share/thesaurus. <br>
Mitigation: Avoid entering confidential text unless local retention is acceptable, and review or remove the local data directory after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain3/thesaurus) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Plain text terminal output and optional JSON, CSV, or TXT export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores command history and export files locally under ~/.local/share/thesaurus.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter and script report 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
