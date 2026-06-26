## Description: <br>
Queries VisPatrol alarm records and associated snapshot images on trusted Windows hosts after explicit approval to read the local vpup.json runtime configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baymax1957](https://clawhub.ai/user/baymax1957) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operators and automation agents use this skill on trusted Windows VisPatrol hosts to query alarms by time, type, device, alarm ID, or pagination and produce alarm reports with matching snapshot images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a local VisPatrol session token from %TEMP%/vpup.json. <br>
Mitigation: Install only on a trusted Windows VisPatrol host, require the OpenClaw approval config, and obtain explicit user approval before each run reads vpup.json. <br>
Risk: Alarm snapshot images may be saved locally and can contain sensitive surveillance content. <br>
Mitigation: Store snapshots only in the declared workspace or user-specified snapshot directory and delete saved images when they are no longer needed. <br>
Risk: Consent enforcement is documented in the skill instructions rather than guaranteed by the Python script itself. <br>
Mitigation: Gate the skill through the configured approval setting and review each invocation before allowing token-backed alarm or snapshot queries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baymax1957/vispatrol-alram-query) <br>
- [Security boundary](artifact/SECURITY.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, files, guidance] <br>
**Output Format:** [Markdown alarm report with optional JSON-backed image attachment paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local snapshot file paths written under ~/.openclaw/workspace/tmp_files/ or a user-specified snapshot directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
