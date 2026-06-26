## Description: <br>
Advanced requirement comprehension and skill orchestration engine that analyzes complex or multi-step user requests, chooses skills to invoke and order, builds task decomposition trees, and delegates memory management and self-iteration to companion skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bustes01](https://clawhub.ai/user/bustes01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to interpret ambiguous or multi-intent requests, decompose them into sub-goals, select appropriate skills, and coordinate sequential or parallel handoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may route complex requests through companion skills with their own memory, logging, cleanup, or delegated-authority behavior. <br>
Mitigation: Review complex-memory-manager and self-iteration-engine before deployment and confirm their behavior fits the intended environment. <br>
Risk: Requirement decomposition or skill selection may produce incorrect, incomplete, or misleading execution plans. <br>
Mitigation: Review orchestration plans before acting on high-impact tasks and ask for clarification when intent, scope, or output format is under-specified. <br>
Risk: The memory reference describes lightweight internal storage patterns that are not appropriate for secrets or personal data. <br>
Mitigation: Keep credentials and sensitive personal data out of skill memory and use environment variables, secret managers, or encrypted system keychains instead. <br>


## Reference(s): <br>
- [Requirement Comprehension Engine on ClawHub](https://clawhub.ai/bustes01/requirement-comprehension-engine) <br>
- [OpenClaw Homepage Metadata](https://clawhub.ai/BusTes01/requirement-comprehension-engine) <br>
- [Orchestration Patterns Reference](references/orchestration-patterns.md) <br>
- [Memory Management Reference](references/memory-management.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with decomposition trees, handoff notes, clarification prompts, and lightweight execution logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May depend on complex-memory-manager and self-iteration-engine for memory conventions, logging, cleanup, and review cycles.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
