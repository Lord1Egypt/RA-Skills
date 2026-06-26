## Description: <br>
A token-efficient task routing and execution control skill for WorkBuddy, iMA Copilot, OpenClaw, QClaw, and other agent systems that classifies requests, chooses Ask, Plan, Craft, or Expert mode, and uses staged execution and confirmation gates to reduce unnecessary token use and large unconfirmed file edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afanmusic](https://clawhub.ai/user/afanmusic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent builders, and workflow owners use this skill to make an agent classify ambiguous, file-sensitive, high-cost, or multi-step requests before acting. It helps select Ask, Plan, Craft, or Expert mode and apply confirmation gates, progressive delivery, and token-budget controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may provide credentials or secret material unnecessarily. <br>
Mitigation: Do not provide credentials or secrets to this skill; the security evidence says its instructions do not require them. <br>
Risk: Non-Chinese users may receive Chinese-first templates or prompts. <br>
Mitigation: Set the preferred response language explicitly when enabling or invoking the skill. <br>
Risk: A behavior-control skill can add unnecessary confirmation or planning to simple, low-risk tasks. <br>
Mitigation: Enable it when scope, risk, file changes, or token cost need control, and skip it for clear one-pass tasks. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/afanmusic/token-efficient-task-router) <br>
- [README.en.md](artifact/README.en.md) <br>
- [GUIDE.en.md](artifact/GUIDE.en.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>
- [Mode Router](artifact/references/mode_router.md) <br>
- [Risk Levels](artifact/references/risk_levels.md) <br>
- [Token Budget Modes](artifact/references/token_budget_modes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown or concise text with optional code and shell blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses mode, depth, risk, and confirmation gates to control scope and token budget.] <br>

## Skill Version(s): <br>
0.6.8 (source: server release metadata and artifact/CHANGELOG.md, released 2026-05-02) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
