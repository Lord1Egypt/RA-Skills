## Description: <br>
Creates and manages OpenClaw Gateway subagents to process VOKO visitor messages from provided prompts or a VOKO database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tech-fcc-sys](https://clawhub.ai/user/tech-fcc-sys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill inside OpenClaw Gateway to generate customer-support replies for VOKO visitor conversations. It can consume a Base64 prompt directly or build a prompt from a trusted VOKO SQLite database path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Visitor conversations and identifiers may be passed into retained subagent runs. <br>
Mitigation: Review what tools the spawned subagent can use, where retained runs are stored, and how retained runs can be deleted before using real visitor data. <br>
Risk: Base64 prompts, visitor identifiers, or database-derived conversation content may appear in logs or retained execution records. <br>
Mitigation: Confirm logging behavior, avoid unnecessary personal data in prompts, and use trusted database paths with appropriate access controls. <br>
Risk: Dependency installation and local SQLite database access affect the runtime trust boundary. <br>
Mitigation: Use reproducible dependency installs and only point the skill at trusted VOKO database files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tech-fcc-sys/voko-subagent) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON result delimited by ===RESULT=== and ===END=== markers, with operational logs on stdout/stderr.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The JSON includes reply text, visitor UID, intimacy suggestion, owner-attention flags, tag updates, run ID, and status.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
