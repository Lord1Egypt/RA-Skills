## Description: <br>
Captures coding errors, anti-patterns, refactoring opportunities, debugging insights, and tooling issues so agents can record and reuse coding learnings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jose-compu](https://clawhub.ai/user/jose-compu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to log lint errors, type mismatches, runtime bugs, anti-patterns, refactoring opportunities, language idiom gaps, debugging insights, and tooling issues. Recurring or broadly useful learnings can be promoted into style guides, lint rules, code snippets, debug playbooks, or reusable skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Learning logs may capture proprietary code context, secrets, or sensitive error output. <br>
Mitigation: Keep .learnings local when it may contain private context, redact secrets and environment values, and prefer short summaries over full stack traces or source files. <br>
Risk: Optional hooks run with the agent's permissions and can surface command output in reminders. <br>
Mitigation: Use opt-in project-level hooks with narrow matchers, start with the lightweight UserPromptSubmit reminder, and avoid logging raw command output. <br>
Risk: Promoted learnings may introduce incorrect guidance into lint configs, AGENTS.md, CLAUDE.md, TOOLS.md, or generated skills. <br>
Mitigation: Review proposed promotions before relying on them and scan generated or modified skills before deployment. <br>


## Reference(s): <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Examples](references/examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jose-compu/self-improving-coding) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and optional hook configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow creates or appends local .learnings markdown files when the agent follows it; optional hooks emit reminder text.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
