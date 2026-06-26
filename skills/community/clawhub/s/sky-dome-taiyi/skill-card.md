## Description: <br>
SkyDome Taiyi / 天穹-太一 is a bilingual AI agent operating-system skill that gives an assistant a named command persona, workflow loop, persistent state and memory protocol, and helper scripts for planning, verification, debugging, research, reporting, and release work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaxia01-1](https://clawhub.ai/user/xiaxia01-1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent builders, and teams using AI assistants can use this skill to structure long-running work with a named persona, evidence-first task loop, reusable playbooks, local state, reviews, reports, and workflow helpers. It is suited to project execution, debugging, research synthesis, documentation, prompt evaluation, and release preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts can create local state, memory, workflow, review, report, lab, and dream files that may contain sensitive project details. <br>
Mitigation: Review generated files before sharing, and avoid running the helpers on repositories, logs, or state directories that contain secrets or private data. <br>
Risk: Diagnostic, log-analysis, benchmarking, and API smoke-test helpers may expose local context, command output, or remote response previews in terminal output or generated reports. <br>
Mitigation: Run helpers only on intended inputs, redact sensitive output before reuse, and prefer synthetic or scrubbed endpoints and logs for testing. <br>
Risk: The skill changes assistant behavior through a strong persona and workflow overlay. <br>
Mitigation: Use it only when that operating style is desired, and keep host platform policy, user instructions, and human review as the controlling authority. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaxia01-1/sky-dome-taiyi) <br>
- [Taiyi Checklists / 太一清单](references/taiyi-checklists.md) <br>
- [Taiyi Patterns / 太一模式库](references/taiyi-patterns.md) <br>
- [Taiyi Practical Playbooks / 太一实战手册](references/taiyi-practical-playbooks.md) <br>
- [Taiyi Workbench Recipes / 太一实用工作流配方库](references/taiyi-workbench-recipes.md) <br>
- [TAIYI_CORE / 太一核心注入](persona/TAIYI_CORE.md) <br>
- [ANTI_DUMB_CORE / 反降智核心](persona/ANTI_DUMB_CORE.md) <br>
- [COGNITION_CORE / 太一高阶认知核心](persona/COGNITION_CORE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, JSON, plain text, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local state, workflow, review, report, lab, memory, checkpoint, and diagnostic files when helper scripts are run by the agent or user.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
