## Description: <br>
Xiaolongxia Memory Manager helps AI agents preserve continuity with a two-track memory system that combines daily Markdown diaries, periodic distillation, and a long-term MEMORY.md file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lg-haha](https://clawhub.ai/user/lg-haha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to configure persistent local memory for AI assistants, including daily logs, long-term memory extraction, session-start context loading, and cross-platform prompt templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The memory workflow can create persistent local records of conversations, preferences, and project context. <br>
Mitigation: Review generated MEMORY.md and memory/*.md files regularly, store only appropriate information, and avoid secrets, credentials, regulated data, or highly sensitive personal details. <br>
Risk: Generated memory files may be unintentionally shared through version control or synced folders. <br>
Mitigation: Keep MEMORY.md and memory/*.md out of shared sync or version control unless sharing is intentional and reviewed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lg-haha/xiaolongxia-memory) <br>
- [Memory Template](references/记忆模板.md) <br>
- [Memory Distillation Example](references/提炼示例.md) <br>
- [General Memory Prompt Template](references/通用prompt模板.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions and prompt templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for local MEMORY.md, memory/YYYY-MM-DD.md, and heartbeat-state.json files when applied by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
