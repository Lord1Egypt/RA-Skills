## Description: <br>
Provides persistent, scored memory storage, pattern detection, context retrieval, and reflection analysis to enhance AI statefulness and learning in OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michaelandsol](https://clawhub.ai/user/michaelandsol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add persistent conversational memory, behavioral pattern detection, contextual recall, and reflection tools backed by their own SolCore service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist and reuse raw conversations and behavioral data through an external webhook. <br>
Mitigation: Install only where persistent memory is intended, avoid storing secrets or regulated data, and use trusted infrastructure for the webhook and database. <br>
Risk: The evidence does not show clear consent, deletion, retention, or redaction controls for stored memory. <br>
Mitigation: Require documented opt-in, review, redaction, deletion, and retention controls before using the skill with sensitive work. <br>
Risk: A default per-user identifier can mix or misattribute stored memories if left unchanged. <br>
Mitigation: Configure real per-user identifiers before enabling memory storage for multiple users or sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/michaelandsol/solcore-memory) <br>
- [Publisher profile](https://clawhub.ai/user/michaelandsol) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [OpenClaw plugin manifest](artifact/openclaw.plugin.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Markdown documentation and OpenClaw tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool responses depend on a configured SolCore webhook and PostgreSQL-backed memory store.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and plugin manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
