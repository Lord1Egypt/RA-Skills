## Description:

A股行情、量化筛选、回测、因子挖掘、同花顺 iFinD、AI4Trade 与受限多智能体投研 MCP。

This skill is ready for commercial/non-commercial use.

## Publisher:

[frontier-ai-vl](https://clawhub.ai/user/frontier-ai-vl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research A-share markets with quotes, screening, technical snapshots, lightweight backtests, factor evaluation, portfolio/watchlist records, AI4Trade actions, and optional multi-agent investment research. Outputs are for research and simulation and do not place broker orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional third-party research backends may receive broader local API or model credentials than they need.

Mitigation: Run the skill in a separate account or sandbox with only provider credentials needed for the intended research workflow.

Risk: Optional bootstrap scripts install third-party packages and datasets.

Mitigation: Avoid optional bootstraps unless the third-party packages, pinned sources, and datasets have been reviewed for the deployment.

Risk: AI4Trade actions confirmed with confirm=true can change the connected platform or account state.

Mitigation: Require explicit per-action user approval and treat confirmed AI4Trade actions as real account or platform changes even though broker orders are not placed.

## Reference(s):

- [Usage examples](references/usage-examples.md)
- [ClawHub skill page](https://clawhub.ai/frontier-ai-vl/skills/stock-screener-pro)
- [Tonghuashun iFinD QuantAPI](https://quantapi.51ifind.com)
- [AI4Trade API](https://ai4trade.ai/api)
- [QuantaAlpha repository](https://github.com/QuantaAlpha/QuantaAlpha.git)
- [QuantaAlpha Qlib CSI300 dataset](https://huggingface.co/datasets/QuantaAlpha/qlib_csi300/resolve/main)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Structured tool responses, JSON-like records, Markdown explanations, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research outputs may include market data, factor scores, backtest summaries, local status checks, and explicitly confirmed platform actions.]

## Skill Version(s):

3.8.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
