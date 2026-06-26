## Description: <br>
Switchgear specification manager for JSON and CSV switchgear tasks, including status checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage local switchgear records from a shell, including adding, listing, searching, removing, exporting, and checking status for entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Entries and configuration values are stored locally in plain text. <br>
Mitigation: Do not store secrets or sensitive operational details in switchgear entries or config values; set SWITCHGEAR_DIR to an appropriate local directory. <br>
Risk: The remove command deletes stored entries by line number. <br>
Mitigation: Review the current entry list and confirm the target line number before removing records. <br>
Risk: Export can overwrite switchgear-export.json or switchgear-export.csv in the current directory. <br>
Mitigation: Run exports from a controlled directory and rename or back up existing export files before exporting. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bytesagain3/switchgear) <br>
- [Publisher Homepage](https://bytesagain.com) <br>
- [Publisher Profile](https://clawhub.ai/user/bytesagain3) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, JSON, CSV] <br>
**Output Format:** [Shell command output with optional JSONL or CSV export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores entries and settings locally under the configured switchgear data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
