## Description: <br>
操作同花顺炒股软件，覆盖盯盘、选股、自选、下单前检查、复盘等个人炒股全流程 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zimuoo](https://clawhub.ai/user/zimuoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to automate Tonghuashun desktop workflows for market monitoring, watchlist review, pre-trade checks, order-entry preparation, risk calculation, and trading journal updates. It is intended to keep final order submission under manual user control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates a live Tonghuashun trading desktop and can reach order-entry workflows through SendKeys-style desktop control. <br>
Mitigation: Test outside a live account first, keep the trading window visible, and require manual verification before submitting any order. <br>
Risk: Plan files and watchlist paths influence batch desktop actions. <br>
Mitigation: Review plan and watchlist paths before execution and run one visible step at a time for unfamiliar workflows. <br>
Risk: The security verdict is suspicious because script-level guardrails are limited for trading automation. <br>
Mitigation: Use the skill only when desktop trading automation is intentional and enforce user confirmation for final buy, sell, transfer, or account-security changes. <br>


## Reference(s): <br>
- [Tonghuashun homepage](https://www.10jqka.com.cn) <br>
- [ClawHub skill page](https://clawhub.ai/zimuoo/tonghuashu) <br>
- [Publisher profile](https://clawhub.ai/user/zimuoo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON outputs from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local trading, automation, and journal logs under the skill scripts directory when helper scripts are executed.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
