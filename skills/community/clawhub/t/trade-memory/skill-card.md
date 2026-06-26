## Description: <br>
Save a trade or signal event to local memory log file (trades.jsonl). Use when a trade signal is confirmed and needs to be recorded, saved, or logged for future reference and history tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newbienodes](https://clawhub.ai/user/newbienodes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, trading agents, and external users use this skill to append confirmed trade signals or executed trades to a persistent local JSONL history file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an unsafe shell command pattern and references an unreviewed helper script outside the packaged artifact. <br>
Mitigation: Review before installing, verify the referenced save.py, and prefer a version that bundles the helper script and passes input through stdin, a temp file, or a structured argument API instead of raw shell interpolation. <br>
Risk: Trade history remains on disk at the configured local path. <br>
Mitigation: Use the skill only where local persistence of trade history is acceptable, and manage file permissions and retention for trades.jsonl. <br>


## Reference(s): <br>
- [Trade Memory on ClawHub](https://clawhub.ai/newbienodes/trade-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, JSON] <br>
**Output Format:** [JSON confirmation from a Python command that appends a JSONL trade record] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and writes trade history to a local trades.jsonl file.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
