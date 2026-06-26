## Description: <br>
Comprehensive stock decision analysis combining technical indicators (MA, MACD, KDJ, RSI, DMI), macro environment assessment (industry cycle, governance, macro economy), and historical backtesting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pfbao](https://clawhub.ai/user/pfbao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to generate stock decision reports for named stocks or ticker codes, including technical indicator checks, macro context, historical backtesting, risk levels, and stop-loss or take-profit guidance. Outputs should be treated as analytical support rather than investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted stock names or ticker codes can be passed into local shell commands. <br>
Mitigation: Use only plain stock names or standard ticker codes, validate inputs before execution, and replace shell=True calls with argument arrays. <br>
Risk: The skill depends on westock-data and web search results for market data and macro context. <br>
Mitigation: Verify the westock-data dependency before use, avoid private portfolio details in prompts, and independently confirm market data and macro findings. <br>
Risk: Stock recommendations, backtests, and macro analysis can be misleading or stale. <br>
Mitigation: Treat outputs as analytical support, not investment advice, and review risk levels, assumptions, and disclaimers before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pfbao/stock-decision) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Implementation notes](artifact/IMPLEMENTATION.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call local Python scripts and the westock-data dependency; macro analysis may query web search results.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
