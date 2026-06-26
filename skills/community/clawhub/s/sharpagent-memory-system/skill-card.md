## Description: <br>
SharpAgent Memory System defines a six-layer agent memory approach with dream processing, TF-IDF retrieval, Chinese tokenization, and persistent JSON or SQLite storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to guide persistent agent memory design, including retention layers, retrieval behavior, storage layout, and memory maintenance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable long-term memory may retain sensitive, stale, or unwanted user information without clear operational controls. <br>
Mitigation: Before use, define what data may be stored, where memory files live, and how users can inspect, export, and purge stored memories. <br>
Risk: Scheduled dream processing can automatically consolidate, archive, forget, or merge memories, changing persistent state without direct user review. <br>
Mitigation: Disable scheduled dream processing or require explicit confirmation unless automatic memory changes are acceptable for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/sharpagent-memory-system) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with tables, architecture diagrams, storage paths, and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes memory layers, persistence locations, retrieval behavior, dream processing, and quality gates.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
