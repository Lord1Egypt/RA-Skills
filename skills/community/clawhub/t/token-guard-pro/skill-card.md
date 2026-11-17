## Description: <br>
Token守护者 helps AI agents reduce token cost with adaptive context compression, semantic caching, model routing, budget guardrails, and cost reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent operators use this skill to manage long conversations, repeated Q&A, model selection, and token budgets while preserving important context such as code, errors, and decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mode changes, cache clearing, model routing, and budget updates can affect cost, latency, or answer quality in shared or cost-sensitive environments. <br>
Mitigation: Review or require confirmation before applying cache, routing, compression-mode, or budget changes. <br>
Risk: Semantic cache behavior or optional embedding services can expose query text or return stale or mismatched cached answers. <br>
Mitigation: Keep sensitive caches local when possible, use conservative similarity thresholds for high-precision tasks, label cached responses, and allow regeneration. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands] <br>
**Output Format:** [Markdown guidance with natural-language commands, slash commands, configuration examples, and operational recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose cache, routing, compression-mode, and budget changes for the host agent to apply.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
