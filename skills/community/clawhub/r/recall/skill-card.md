## Description: <br>
Recall teaches agents to check local context, use knowledge access patterns, maintain memory, and resist hallucination before answering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crewhaus](https://clawhub.ai/user/crewhaus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Recall to help agents inspect workspace context, skills, tools, and memory before answering or acting. It is intended for agents that benefit from proactive context loading, source checking, and concise uncertainty handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages proactive local context and memory use, which can surface stale, sensitive, or overly broad workspace information if left unmanaged. <br>
Mitigation: Review memory, TOOLS.md, and task files periodically, avoid storing secrets or sensitive personal details, and limit proactive reads to files intended for agent consumption. <br>
Risk: Tool-first behavior can lead an agent toward high-impact actions such as sending messages, posting publicly, spending money, or modifying important data. <br>
Mitigation: Require explicit operator confirmation before using tools that communicate externally, spend money, or change important data. <br>


## Reference(s): <br>
- [Knowledge-Driven Agent certification](https://crewhaus.ai/certify) <br>
- [Anti-patterns](references/anti-patterns.md) <br>
- [Knowledge patterns](references/knowledge-patterns.md) <br>
- [Session checklist](references/session-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text] <br>
**Output Format:** [Markdown instructions and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; no scripts or runtime API calls.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
