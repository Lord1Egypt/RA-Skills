## Description: <br>
Create, modify, and debug agentic Squid pipelines that define multi-agent YAML workflows with spawns, gates, parallel execution, loops, branching, restart loops, sub-pipelines, and structured approvals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dominno](https://clawhub.ai/user/dominno) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to author, modify, validate, and test Squid YAML workflows that coordinate shell commands, agent spawns, human approvals, and sub-pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Squid pipelines can execute local commands, spawn agents, mutate repositories, and trigger deployment or publishing workflows. <br>
Mitigation: Run generated or included pipelines in a sandbox or clean branch, inspect each run command, restrict repo and output paths, and require gate approvals before side effects. <br>
Risk: Examples and generated workflows may include high-impact repository mutation, npm scripts, pull request creation, or deployment patterns. <br>
Mitigation: Avoid untrusted npm scripts, review diffs before approving commits or pull requests, and keep production deploy or publish steps behind explicit human approval. <br>


## Reference(s): <br>
- [Step Types Reference](references/step-types.md) <br>
- [Workflow Patterns](references/patterns.md) <br>
- [Testing Reference](references/testing.md) <br>
- [Getting Started](https://raw.githubusercontent.com/dominno/squid/refs/heads/main/docs/getting-started.md) <br>
- [Agent Adapters](https://raw.githubusercontent.com/dominno/squid/refs/heads/main/docs/adapters.md) <br>
- [Squid Workflow Examples](https://github.com/dominno/squid-workflows) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML, TypeScript, and shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include executable pipeline definitions and commands that require human review before use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
