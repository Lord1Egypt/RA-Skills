## Description: <br>
Orchestrates a dynamic multi-agent team where a lead agent plans and delegates tasks to specialized worker agents that communicate bidirectionally for parallel or specialized workstreams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aa-rick](https://clawhub.ai/user/aa-rick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to split complex tasks into two to four specialized worker streams, coordinate bidirectional worker communication, and synthesize the results into a final answer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation language could start delegated multi-agent workflows for sensitive tasks without clear user opt-in. <br>
Mitigation: Enable this skill only for tasks that intentionally require multi-agent orchestration, and avoid using it as a default handler for routine writing, debugging, code review, research, or trading questions. <br>
Risk: Worker agents may receive private code, logs, credentials, regulated data, or other sensitive context. <br>
Mitigation: Pass only the minimum context each worker needs, redact secrets before delegation, and use the skill only where controls exist for what each worker receives and how long sessions persist. <br>
Risk: Market research or trading signal analysis may be mistaken for financial advice. <br>
Mitigation: Treat outputs as informational analysis and require qualified human review before making trading, investment, or other financial decisions. <br>


## Reference(s): <br>
- [Role Patterns](references/role-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/aa-rick/xqe-agent-team) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or structured text with delegated worker findings, progress updates, and a synthesized final answer.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the delegated task and may include role plans, worker instructions, analysis, code review findings, market research, trading signal analysis, debugging guidance, or document drafts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
