## Description: <br>
Trigger helps agents use a local command-line productivity logger for everyday task, planning, review, tagging, search, status, and export workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and command-line users use Trigger to capture local productivity notes, review recent activity, inspect simple statistics, search logs, and export records for later review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trigger stores user-entered entries and exported history in local files. <br>
Mitigation: Avoid entering passwords, API keys, private client data, or other secrets, and review or delete local logs and exports when they are no longer needed. <br>
Risk: The documented TRIGGER_DIR setting does not appear to be honored by the script. <br>
Mitigation: Assume data is written under ~/.local/share/trigger unless the script is updated and verified in the target environment. <br>


## Reference(s): <br>
- [Trigger on ClawHub](https://clawhub.ai/ckchzh/trigger) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text CLI output, with optional JSON, CSV, or TXT exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local log and export files under ~/.local/share/trigger.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
