## Description: <br>
Scar memory, reflex arc, and decision traces for AI agents that learn from failures, block repeated mistakes without LLM calls, and export judgment traces for training data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aibenyclaude-coder](https://clawhub.ai/user/aibenyclaude-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent engineers use this skill to give agents local scar memory, pre-action reflex checks, narrative handoff records, decision traces, and lightweight safety audits for code and CI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included CI action and repository-audit tooling can inspect broad source trees or remote repositories. <br>
Mitigation: Review the action before installation, pin it to a reviewed tag or commit, use fixed trusted inputs, and prefer local-only scans unless the repository URL is trusted. <br>
Risk: Scar, narrative, decision-trace, and training JSONL files can contain sensitive project data. <br>
Mitigation: Keep memory and training files protected as project data and avoid recording secrets or credentials. <br>
Risk: Pattern-based reflex and audit checks may miss hazards or block benign work. <br>
Mitigation: Use the results as pre-execution signals and manually review blocked or high-impact actions before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aibenyclaude-coder/tetra-scar) <br>
- [Publisher profile](https://clawhub.ai/user/aibenyclaude-coder) <br>
- [README](artifact/README.md) <br>
- [GitHub Action metadata](artifact/action.yml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [CLI text, JSON/JSONL files, Markdown reports, Python API outputs, and GitHub Actions summary fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local append-only memory files and audit reports may contain sensitive project context.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata; artifact frontmatter says 0.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
