## Description: <br>
Self-improving AI agent loop that runs Brainstorm, Plan, Implement, Review, Verify, and Evolve cycles with local safety monitoring and rollback controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nefas11](https://clawhub.ai/user/Nefas11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run supervised local code-evolution cycles against a target file, with metric-driven verification, git rollback, reputation scoring, monitor logs, and optional alerting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The autonomous code loop has broad local mutation authority and some advertised safety boundaries may be under-enforced. <br>
Mitigation: Run only in a disposable clone or clean worktree, then review diffs, verification output, and monitor logs before keeping changes. <br>
Risk: Metric commands and provided agent or LLM callables are trusted code paths. <br>
Mitigation: Use only trusted metric commands and agent callables, and avoid running the skill in repositories with valuable uncommitted work. <br>
Risk: Optional Telegram alerts or remote LLM review can send alert or session details outside the machine. <br>
Mitigation: Leave MONITOR_TELEGRAM_BOT_TOKEN and MONITOR_LLM_COMMAND unset unless that external disclosure is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/Nefas11/supervised-agentic-loop) <br>
- [Source repository from ClawHub metadata](https://github.com/Nefas11/supervised-agentic-loop) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python examples, configuration notes, and local state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write results.tsv and .state files for reputation, learnings, tool-call logs, monitor alerts, and heartbeat data.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
