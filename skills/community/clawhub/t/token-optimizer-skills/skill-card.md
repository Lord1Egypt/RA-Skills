## Description: <br>
Full token economy suite for OpenClaw agents that audits context-window usage across skills, history, and tool outputs, then applies token-reduction strategies without losing memory quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[legiovi](https://clawhub.ai/user/legiovi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to audit token usage, identify context bloat, count or estimate prompt tokens, distill long conversations into JSON memory facts, and choose compression strategies for large prompts or documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist conversation-derived memory to disk. <br>
Mitigation: Require explicit user approval before memory writes or context flushes, and review distilled facts before treating them as durable memory. <br>
Risk: The orchestration layer can run configured local Python helper scripts. <br>
Mitigation: Keep the tool registry narrow, review configured script paths before installation, and disable orchestration files if only token counting is needed. <br>
Risk: Tokenizer or compression helpers may require remote package or model downloads. <br>
Mitigation: Use estimate mode in sensitive environments, preinstall trusted tokenizer packages, or avoid remote tokenizer and model downloads. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/legiovi/token-optimizer-skills) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Memory persistence patterns](artifact/memory-persistence-patterns.md) <br>
- [Gemma optimization guide](artifact/gemma-optimization.md) <br>
- [Token audit reference](artifact/token_audit.md) <br>
- [Token optimizer strategies](artifact/token_optimizer_strategies.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON memory facts, shell command guidance, and local script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local skill metadata and conversation-history files, run local Python helper scripts, and write distilled memory files when configured.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
