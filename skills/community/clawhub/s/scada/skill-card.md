## Description: <br>
Supervisory control and data acquisition manager. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill as a local CLI helper to add, list, search, remove, export, and summarize simple timestamped entries. Do not use it for real SCADA monitoring, device control, safety workflows, or operational assurance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is advertised as SCADA industrial-control management, but the security evidence describes it as a simple local log manager. <br>
Mitigation: Use it only as a local entry/log helper; do not rely on it for monitoring, device control, safety workflows, or operational assurance. <br>
Risk: Entries and exports may contain sensitive operational details. <br>
Mitigation: Avoid storing secrets or sensitive operational information, and review JSONL or CSV exports before sharing them. <br>
Risk: Removal is immediate and local exports write files to the current working directory. <br>
Mitigation: Confirm entry numbers before removal and verify export destination and contents after running export commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/scada) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, configuration] <br>
**Output Format:** [Structured stdout text with local JSONL or CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores data under ~/.scada by default; SCADA_DIR can set a different local data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
