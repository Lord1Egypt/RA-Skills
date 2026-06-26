## Description: <br>
Enterprise-grade OpenClaw skill for cleaning up orphaned subagent processes, archiving transcripts to SuperMemory, and freeing disk space without losing work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LvcidPsyche](https://clawhub.ai/user/LvcidPsyche) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operations teams use this skill to inspect OpenClaw subagent sessions, preview cleanup candidates, archive transcripts, and remove orphaned session files using configurable retention policies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release instructs users to run a cleanup script that is not present in the artifact, and that script would delete and possibly archive private session data. <br>
Mitigation: Review or obtain the missing implementation from a trusted source before running it; start with dry-run mode and keep independent backups. <br>
Risk: Cleanup options such as forced deletion or cleanup without archival can cause data loss. <br>
Mitigation: Avoid --force and --no-archive unless data loss has been explicitly accepted; confirm retention thresholds and deletion counts before enabling scheduled cleanup. <br>
Risk: Archival can send session transcripts to external storage or SuperMemory, which may expose private session content. <br>
Mitigation: Confirm exactly what session data will be archived, verify archive destination settings, and enable external archival only after reviewing data handling requirements. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/LvcidPsyche/swarm-janitor) <br>
- [Configuration reference](references/config.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and YAML configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce cleanup reports in text, JSON, or CSV when the referenced implementation is available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
