## Description: <br>
Tagout is a shell-based safety compliance tracker for recording, listing, searching, exporting, and checking tagout tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, safety coordinators, and operators use Tagout to maintain a local record of tagout-related tasks, check status, search entries, remove entries, and export records to JSON or CSV. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Removing an entry immediately deletes that local record. <br>
Mitigation: Back up the TAGOUT_DIR data or exported records before using remove, and verify the target line number first. <br>
Risk: Entries and exported files may expose sensitive operational details if users enter secrets or share exports broadly. <br>
Mitigation: Do not store secrets in entries, choose TAGOUT_DIR deliberately, and review exported JSON or CSV files before sharing them. <br>


## Reference(s): <br>
- [ClawHub Tagout](https://clawhub.ai/bytesagain1/tagout) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Plain text command output with local JSONL records and optional JSON or CSV exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TAGOUT_DIR when set, otherwise stores records under ~/.tagout; export writes tagout-export.json or tagout-export.csv in the working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
