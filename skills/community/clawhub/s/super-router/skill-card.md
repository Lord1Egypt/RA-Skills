## Description: <br>
LangGraph task router for OpenClaw that decomposes complex work into dependency-aware subtasks, routes each branch to PRO or FLASH models, retries or escalates failures, and records token usage for auditable runs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanyadan](https://clawhub.ai/user/fanyadan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Super Router to decompose complex OpenClaw tasks, route subtasks across configured model roles, manage dependency-aware execution, and preserve audit and token-usage records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The router can pass task text and derived context to configured model providers and optional telemetry. <br>
Mitigation: Review provider and LangSmith settings before use; keep prompt and output previews disabled unless needed for a trusted workflow. <br>
Risk: The router can run provider CLIs with broad local environment access and Gemini CLI auto-approval behavior. <br>
Mitigation: Use trusted provider CLIs, review or disable Gemini auto-approval before sensitive use, and avoid remote Ollama endpoints unless they are trusted. <br>
Risk: Saved prompts, logs, ledgers, and generated artifacts may contain sensitive task data. <br>
Mitigation: Store run artifacts in protected locations, review them before sharing, and remove sensitive logs when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fanyadan/skills/super-router) <br>
- [LangGraph documentation](https://langchain-ai.github.io/langgraph/) <br>
- [Ollama documentation](https://ollama.com/docs) <br>
- [Background Router Artifact Launches](references/background-artifact-launches.md) <br>
- [Recovering Gemini CLI Token Usage](references/gemini-cli-token-recovery.md) <br>
- [Source-to-HTML Background Router Wrapper](references/source-html-background-wrapper.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, CLI output, optional JSONL usage ledgers, and generated local artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include provider trace metadata, token usage summaries, run logs, and generated files when configured.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
