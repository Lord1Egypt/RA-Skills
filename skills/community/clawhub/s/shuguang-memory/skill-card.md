## Description: <br>
曙光记忆系统 provides a local five-layer persistent memory system for agents with tiered retention, hybrid retrieval, WAL-style writes, and self-improvement logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chen6896qqwee](https://clawhub.ai/user/chen6896qqwee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add local, cross-session memory for preferences, facts, decisions, entities, reflections, and lessons. It is suited to agents that need recall, archiving, and memory maintenance without an external database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist broad user and agent information long term in local memory files. <br>
Mitigation: Require explicit confirmation before saving memories, and avoid storing secrets or regulated data. <br>
Risk: Global or poorly scoped memory may mix information across users, projects, or tasks. <br>
Mitigation: Prefer project- or user-specific scopes and separate memory directories for distinct contexts. <br>
Risk: Generated memory files may remain after the user expects a session to be forgotten. <br>
Mitigation: Periodically inspect and delete generated memory files under the OpenClaw workspace or configured memory directory. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chen6896qqwee/shuguang-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with Python code examples and local JSON/Markdown memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores memory locally under the configured workspace or memory directory when its Python code is used.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
