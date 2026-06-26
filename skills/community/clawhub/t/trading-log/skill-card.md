## Description: <br>
Trading Log records stock buy and sell activity, tracks positions and profit/loss, and can refresh live A-share and Hong Kong quote data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wtjjacobj](https://clawhub.ai/user/wtjjacobj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or agents use this skill to record A-share and Hong Kong stock trades, view current positions, and generate profit/loss summaries from a local trading log. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive trading history is stored permanently in local JSON files. <br>
Mitigation: Use only on a trusted device, verify the configured data path before running, and manage the JSON file according to the user's retention needs. <br>
Risk: Live quote lookup sends stock codes to Tencent and may return incomplete or unavailable prices. <br>
Mitigation: Confirm external quote access is acceptable and verify prices before relying on generated profit/loss summaries. <br>
Risk: Broad trade-related triggers can mutate financial records without clear controls. <br>
Mitigation: Ask for explicit confirmation before recording, selling, clearing, or editing trades, and review the latest log after each mutation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wtjjacobj/trading-log) <br>
- [Tencent quote endpoint used by the skill](https://qt.gtimg.cn/q=sh600519,sz000001) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON files, Guidance] <br>
**Output Format:** [Command-line text reports and local JSON records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores trading history and daily profit/loss summaries in local JSON files; live quote refresh sends stock codes to Tencent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
