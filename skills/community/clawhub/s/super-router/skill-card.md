## Description:

LangGraph task router for OpenClaw that decomposes complex work into dependency-aware subtasks, routes each branch to PRO or FLASH models, retries or escalates failures, and records token usage for auditable runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanyadan](https://clawhub.ai/user/fanyadan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to break complex requests into dependency-aware subtasks, route each branch to an appropriate model role, and produce auditable execution reports with retry, escalation, and token-usage details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The router may send task text and project context to configured model providers.

Mitigation: Use a dedicated environment with minimal secrets, prefer local-only Ollama for sensitive work, and keep LangSmith prompt and output tracing off unless the data is appropriate for external tracing.

Risk: The skill uses broad local execution and environment-based provider configuration.

Mitigation: Review local execution behavior before installation and avoid placing unrelated credentials in ~/.openclaw/.env.

Risk: Untrusted task text may be unsafe until shell-invocation examples and Gemini auto-approval behavior are hardened.

Mitigation: Do not route untrusted task text through the skill until those behaviors have been reviewed and hardened.

## Reference(s):

- [Super Router on ClawHub](https://clawhub.ai/fanyadan/skills/super-router)
- [Publisher profile](https://clawhub.ai/user/fanyadan)
- [LangGraph documentation](https://langchain-ai.github.io/langgraph/)
- [Ollama documentation](https://ollama.com/docs)
- [Gemini CLI headless JSON output](https://google-gemini.github.io/gemini-cli/docs/cli/headless.html)
- [Linux mm Source-to-HTML Hierarchy Example](references/linux-mm-source-html-example.md)
- [Recovering Gemini CLI token usage when super-router ledger is unavailable](references/gemini-cli-token-recovery.md)
- [Gemini CLI ripgrep Detection Fix](references/gemini-cli-ripgrep-path-fix.md)
- [Gemini Temperature Gap in generate_text()](references/gemini-temperature-gap.md)
- [Long-Running Quantitative Tasks with Super-Router](references/long-running-quantitative-tasks.md)
- [Background Router Artifact Launches](references/background-artifact-launches.md)
- [Source-to-HTML Background Router Wrapper](references/source-html-background-wrapper.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or text reports with JSON-serializable router state and inline shell/configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include planned subtasks, model route decisions, execution results, fallback status, audit history, final reports, and token-usage summaries.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
