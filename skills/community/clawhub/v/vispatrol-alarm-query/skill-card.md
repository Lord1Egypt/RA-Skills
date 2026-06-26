## Description: <br>
Queries VisPatrol alarm records and latest alarm snapshots on a trusted Windows host after explicit approval to read the local %TEMP%/vpup.json session file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baymax1957](https://clawhub.ai/user/baymax1957) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to turn natural-language alarm requests into bounded VisPatrol alarm queries, then summarize returned alarms with matching local snapshot attachments. It is intended for trusted Windows environments that already run VisPatrol and have approved access to %TEMP%/vpup.json. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a local VisPatrol session token from %TEMP%/vpup.json for alarm and snapshot queries. <br>
Mitigation: Install only on trusted Windows hosts that already run VisPatrol, require explicit user approval before each run, and keep token use limited to read-only alarm and snapshot requests. <br>
Risk: One snapshot download path can send the local session token outside the documented VisPatrol endpoint boundary. <br>
Mitigation: Before broad deployment, restrict snapshot downloads to the configured VisPatrol media host or avoid sending the bearer token to absolute snapshot URLs. <br>
Risk: Snapshot images are saved locally after queries. <br>
Mitigation: Store snapshots only in the documented workspace temporary directory or an explicitly configured snapshot output directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baymax1957/vispatrol-alarm-query) <br>
- [Security boundary](SECURITY.md) <br>
- [Skill instructions](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Configuration] <br>
**Output Format:** [Markdown alarm report with optional local snapshot image attachments; JSON may be used as script output for agent processing.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python on Windows, VisPatrol runtime configuration at %TEMP%/vpup.json, and dependencies requests, cryptography, and pycryptodome.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
