## Description: <br>
A safe AI agent evolution engine that analyzes runtime history to identify improvements and applies protocol-constrained evolution with comprehensive safety checks and audit logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[confidentkai](https://clawhub.ai/user/confidentkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use Safe Evolver to record local agent interaction history, analyze behavior changes, and generate improvement suggestions for review before applying them to an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local history and log files may contain sensitive prompts, responses, commands, paths, or other data passed to recordInteraction. <br>
Mitigation: Do not record secrets, credentials, regulated data, private file contents, or raw sensitive prompts and responses; configure log and history paths in controlled local directories. <br>
Risk: Generated improvement suggestions may be incorrect or unsuitable for a production agent workflow. <br>
Mitigation: Keep code, command, and workflow changes behind explicit human review and scanning before deployment. <br>
Risk: Some documented LLM, export, and apply APIs are examples that are not implemented in the provided JavaScript artifact. <br>
Mitigation: Verify available APIs against the installed package before integration and perform separate security review for any new LLM, export, or apply implementation. <br>


## Reference(s): <br>
- [Safe Evolver on ClawHub](https://clawhub.ai/confidentkai/safe-evolver) <br>
- [confidentkai publisher profile](https://clawhub.ai/user/confidentkai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [JavaScript objects, JSON history/log files, and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local log and history files at configurable paths.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
