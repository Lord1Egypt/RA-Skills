## Description: <br>
Synapse augments OpenClaw's built-in memory tools with structured learning, preference tracking, pattern detection, and cross-session intelligence consolidation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shadoprizm](https://clawhub.ai/user/shadoprizm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent operators use Synapse to maintain a local structured profile of facts, preferences, behavioral patterns, corrections, and daily learning summaries across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically read prior conversations and build persistent local profiles without clear opt-in, review, or deletion controls. <br>
Mitigation: Require user confirmation before profile writes, narrow trigger phrases, and periodically review or delete generated Synapse memory files. <br>
Risk: Persistent memory files may collect preferences, behavioral patterns, and other operator information over time. <br>
Mitigation: Set a controlled SYNAPSE_DATA_DIR, keep storage local, and avoid storing credentials, tokens, passwords, or other sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shadoprizm/synapse-memory) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown summaries plus local JSON and JSONL memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill that uses local OpenClaw memory and file tools; no network calls or external credentials are declared.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
