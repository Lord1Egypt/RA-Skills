## Description: <br>
Token消耗监控优化 helps QClaw/OpenClaw users inspect local session logs, summarize token use, detect abnormal spending patterns, and generate optimization guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QClaw/OpenClaw users use this skill to review token consumption, identify spikes or repeated failures, and choose practical changes that reduce waste. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local QClaw/OpenClaw session logs can contain prompts, responses, or other sensitive text. <br>
Mitigation: Run the skill only when comfortable inspecting those local logs, and review any generated reports before sharing them. <br>
Risk: The referenced token_stats.py helper is not bundled in this release. <br>
Mitigation: Inspect the local token_stats.py script before executing the documented commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/qclaw-token-monitor) <br>
- [freedompixels publisher profile](https://clawhub.ai/user/freedompixels) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with shell command examples and tabular token summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local token usage reports from QClaw/OpenClaw session logs.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
