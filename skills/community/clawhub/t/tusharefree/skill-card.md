## Description: <br>
Provides Tushare Pro financial-data API guidance for A-shares, indices, funds, futures, bonds, macroeconomic data, and token-authenticated Python access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coderwpf](https://clawhub.ai/user/coderwpf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and agents use this skill to configure the Tushare Python API and retrieve Chinese financial market, company financial, fund, futures, bond, and macroeconomic data for analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tushare tokens are account credentials and can be exposed if hardcoded in prompts, scripts, or shared notebooks. <br>
Mitigation: Use TUSHARE_TOKEN or a secret manager, avoid committing tokens, and rotate any token that may have been exposed. <br>
Risk: Unpinned Python dependencies can change behavior or introduce supply-chain risk in production and shared environments. <br>
Mitigation: Pin and review dependency versions before deployment, especially for tushare and pandas. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/coderwpf/tusharefree) <br>
- [Tushare Pro](https://tushare.pro) <br>
- [Tushare Pro Documentation](https://tushare.pro/document/2) <br>
- [Tushare API Interface List](https://tushare.pro/document/1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a Tushare token; examples produce pandas DataFrames and optional CSV files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
