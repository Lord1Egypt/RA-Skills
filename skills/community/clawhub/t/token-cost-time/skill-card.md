## Description: <br>
Estimates LLM task token usage, cost, and duration using rule-based classification, baseline priors, and optional local profile data without external dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[highnoonoffice](https://clawhub.ai/user/highnoonoffice) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to estimate token usage, cost, duration, and model tradeoffs for LLM tasks, then improve estimates by recording local execution data over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local usage logs and profile data are written under ~/.token-cost-time by default. <br>
Mitigation: Treat those files as private workflow metadata, review the recorded fields, and delete or relocate the directory if historical usage data should not be retained. <br>
Risk: Cold-start estimates rely on baseline priors before enough local runs have been recorded. <br>
Mitigation: Use the reported confidence value when interpreting estimates and record representative runs before relying on personalized cost or duration projections. <br>


## Reference(s): <br>
- [Token Cost Time ClawHub page](https://clawhub.ai/highnoonoffice/token-cost-time) <br>
- [Self-Improvement Guide](references/self-improvement.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [JSON CLI and library responses, plus local JSON and JSONL profile files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Records profile and execution history under ~/.token-cost-time by default unless a custom profile path is provided.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
