## Description: <br>
OpenClaw skill for LangGraph-based task routing between PRO and FLASH models for task decomposition, parallel fanout, structured complexity scoring, and FLASH-to-PRO escalation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanyadan](https://clawhub.ai/user/fanyadan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to split complex tasks into atomic subtasks, score their complexity, route them between fast and stronger model backends, and return an auditable final report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task text, intermediate outputs, and finalization context may be sent to the configured Gemini CLI or Ollama model provider. <br>
Mitigation: Use trusted provider endpoints for sensitive work, prefer local Ollama where appropriate, isolate the runtime, and avoid debug output when prompts may contain secrets. <br>
Risk: Model-generated route outputs or final reports may be incomplete or incorrect for high-impact production, billing, security, or rollback decisions. <br>
Mitigation: Review the route audit trail, fallback details, and final report before acting on recommendations or applying downstream changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fanyadan/super-router) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [LangGraph documentation](https://langchain-ai.github.io/langgraph/) <br>
- [Ollama documentation](https://ollama.com/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON-serializable router state and human-readable final report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes planned subtasks, route decisions, execution results, fallback metadata, and finalizer outcome when available.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
