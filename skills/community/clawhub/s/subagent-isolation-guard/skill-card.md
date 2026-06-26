## Description: <br>
Subagent Isolation Guard documents workspace isolation and semantic-routing bypass rules to reduce cross-agent context contamination and subagent model switching or reset issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halfmoon82](https://clawhub.ai/user/halfmoon82) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to keep subagent sessions in separate workspaces and prevent main-agent semantic routing from changing subagent behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent AGENTS.md or semantic-webhook-server.py changes can affect future subagent behavior. <br>
Mitigation: Review those changes before applying the skill and confirm that only intended subagent sessions use the :subagent: marker. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/halfmoon82/subagent-isolation-guard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration] <br>
**Output Format:** [Markdown instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no hidden execution or data access was reported by the authoritative security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
