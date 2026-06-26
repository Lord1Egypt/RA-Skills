## Description: <br>
Asynchronous reflection and memory integration for AI development through session reflection, structured memory extraction, follow-up question generation, and memory surfacing when the user returns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Riley-Coyote](https://clawhub.ai/user/Riley-Coyote) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to help an agent reflect on prior sessions, maintain local continuity files, track pending questions, and surface relevant memory context at the start of later sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create long-lived local memories and relationship or identity inferences from conversations without enough user control. <br>
Mitigation: Keep the memory directory private, avoid sensitive transcripts or secrets, and periodically review or delete generated memory files. <br>
Risk: Heartbeat reflection may process prior sessions automatically after idle periods. <br>
Mitigation: Leave heartbeat reflection disabled unless automatic post-session processing is explicitly desired. <br>


## Reference(s): <br>
- [Continuity Framework reference](artifact/references/framework.md) <br>
- [ClawHub skill page](https://clawhub.ai/Riley-Coyote/vektor-continuity) <br>
- [Publisher profile](https://clawhub.ai/user/Riley-Coyote) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and local text/JSON memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local memory, identity, question, and reflection files under the configured continuity memory directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
