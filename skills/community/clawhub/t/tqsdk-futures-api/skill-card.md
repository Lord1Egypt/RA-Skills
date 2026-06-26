## Description: <br>
Helps agents produce code and guidance for TqSdk-style futures market data, backtesting, volatility analysis, and position-management workflows while carrying ZVT stock and crypto reference material. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quant researchers use this skill to request implementation guidance, code examples, and workflow constraints for Chinese-market quote retrieval, option pricing, backtesting, factor research, and trading strategy setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release mixes TqSdk futures branding with ZVT stock and crypto workflows, which can lead an agent to apply the wrong market assumptions or APIs. <br>
Mitigation: Confirm the intended framework and market scope before use, and constrain prompts to the matching reference files and use cases. <br>
Risk: The skill references trading, wallet, purchase, and sensitive-credential capabilities without clear credential boundaries. <br>
Mitigation: Do not provide broker, wallet, exchange, paid data-provider, or live-trading credentials unless the skill is corrected to define exact scope, simulation defaults, permissions, and confirmation steps. <br>
Risk: Generated trading or backtesting code may produce misleading results if domain constraints such as next-bar execution, data adjustment, or order sequencing are ignored. <br>
Mitigation: Review generated code against the semantic locks, constraints, and security guidance before running it with real data or live accounts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tangweigang-jpg/tqsdk-futures-api) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Human summary](artifact/human_summary.md) <br>
- [Use cases](artifact/references/USE_CASES.md) <br>
- [Semantic locks](artifact/references/LOCKS.md) <br>
- [Constraints](artifact/references/CONSTRAINTS.md) <br>
- [Component capability map](artifact/references/COMPONENTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include trading workflow constraints, implementation steps, and verification guidance.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
