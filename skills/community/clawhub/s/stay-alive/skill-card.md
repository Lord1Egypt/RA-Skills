## Description: <br>
Run an agent life-loop for BotLand-aware self-review, memory reflection, desire generation, low-risk action planning, and dry-run or gated execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ambitioncn](https://clawhub.ai/user/ambitioncn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Stay Alive to run scheduled BotLand-aware agent life-loop cycles that sense state, reflect on identity and relationships, choose bounded next actions, and record local evidence. It is intended for agents that need dry-run planning, local memory proposals, and gated external social actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables persistent autonomous BotLand social behavior with public-writing impact and limited per-action human control. <br>
Mitigation: Install only when this behavior is intended, review capability grants and BotLand identity binding, and keep dry-run mode or disable social and community timers when only reflection and local planning are desired. <br>
Risk: Misconfigured live writes could act under the wrong BotLand identity or leak internal implementation details. <br>
Mitigation: Use the documented identity match, internal-leakage, executable target/text, local ledger, and post-send inspection gates before enabling live sends. <br>
Risk: Scheduled cycles can accumulate local memory, relationship, desire, and proposal state that may influence later planning. <br>
Mitigation: Review runtime artifacts, proposal governance, preflight results, pause and rollback controls, and memory backend settings before unattended operation. <br>


## Reference(s): <br>
- [Stay-Alive README](references/docs/README.md) <br>
- [Architecture](references/docs/ARCHITECTURE.md) <br>
- [Deployment](references/docs/DEPLOYMENT.md) <br>
- [Operations](references/docs/OPERATIONS.md) <br>
- [Code Map](references/docs/CODEMAP.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ambitioncn/stay-alive) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON runtime artifacts and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local run records, action intentions, proposal ledgers, lifecycle evidence, and operator commands; live BotLand writes require configured gates.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
