## Description: <br>
X2Strategy helps agents convert quantitative finance research inputs into structured strategy specifications, generated Backtrader code, backtest outputs, and diagnosis reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patrick-lew](https://clawhub.ai/user/patrick-lew) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, quant researchers, and trading-system builders use this skill to extract strategy logic from finance papers or drafts, generate executable Backtrader implementations, validate them, run backtests, and compare results against paper-reported metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store credentials and documents and send document excerpts to configured external LLM providers. <br>
Mitigation: Use a managed secret mechanism when possible and avoid confidential or unpublished documents unless sending excerpts to the configured provider is acceptable. <br>
Risk: The skill can generate and run trading or backtest code. <br>
Mitigation: Review generated strategy code before execution and run it in an isolated workspace or container. <br>
Risk: Bundled test tooling may load credentials and perform live API or network tests. <br>
Mitigation: Do not run the full-test script unless live tests are intentional and the loaded credentials have been reviewed. <br>


## Reference(s): <br>
- [X2Strategy ClawHub listing](https://clawhub.ai/patrick-lew/x2strategy) <br>
- [paper2spec reference](references/paper2spec.md) <br>
- [spec2code reference](references/spec2code.md) <br>
- [skill internals reference](references/skill-internals.md) <br>
- [Backtrader patterns](references/backtrader_patterns.md) <br>
- [Data sources](references/data_sources.md) <br>
- [Architecture](docs/ARCHITECTURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with generated Python code, JSON specifications, shell commands, and backtest summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local analysis artifacts such as content.json, spec.json, spec.md, strategy.py, metadata.json, and diagnosis reports.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
