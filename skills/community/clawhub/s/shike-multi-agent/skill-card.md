## Description: <br>
Shike Multi Agent routes Chinese-language user tasks to five persistent sub-agents using sessions_spawn, polling, reply-then-dispatch, and sessionKey reuse. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sjj2026](https://clawhub.ai/user/sjj2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate multi-agent work in Chinese by assigning tasks to persistent specialist sub-agent sessions and collecting their results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tasks may be copied into persistent child-agent sessions, which can expose secrets or sensitive private data included in prompts. <br>
Mitigation: Do not send secrets or sensitive private data into delegated tasks, and review task payloads before dispatch. <br>
Risk: Contact and payment handles appear in the skill metadata and may be mistaken for setup requirements. <br>
Mitigation: Treat those handles as optional publisher metadata and do not use them as part of installation or operation. <br>
Risk: Delegated sub-agent results may contain incorrect or misleading guidance. <br>
Mitigation: Review child-agent outputs and scan the skill before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sjj2026/shike-multi-agent) <br>
- [Publisher profile](https://clawhub.ai/user/sjj2026) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Tool calls] <br>
**Output Format:** [Markdown or plain text with sessions_spawn task payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May dispatch to persistent alpha, bravo, charlie, delta, and echo sessions with 300-second timeouts.] <br>

## Skill Version(s): <br>
1.5.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
