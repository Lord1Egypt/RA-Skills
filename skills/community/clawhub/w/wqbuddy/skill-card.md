## Description: <br>
Provides CLI tools and a specialized Alpha Miner sub-agent for WorldQuant BRAIN workflows including alpha backtesting, field search, dataset browsing, operator lookup, progress checks, and alpha submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sebrinass](https://clawhub.ai/user/sebrinass) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative researchers use WQBuddy to run WorldQuant BRAIN CLI workflows for alpha backtesting, field exploration, dataset and operator lookup, competition progress checks, and managed alpha submission. For larger field exploration or iterative strategy work, it can guide an agent through the packaged Alpha Miner workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores WorldQuant BRAIN account credentials and session tokens in local files. <br>
Mitigation: Protect the configuration and token files, avoid syncing them, and periodically review or delete stored credentials and tokens. <br>
Risk: The Alpha Miner workflow loads external agent instructions from the installed npm package. <br>
Mitigation: Install only if the package and publisher are trusted, and inspect the installed agent files before spawning the Alpha Miner. <br>
Risk: The workflow includes alpha submission and other account-changing BRAIN actions without clear approval controls. <br>
Mitigation: Require explicit user approval before any alpha submission or other account-changing BRAIN action. <br>
Risk: The skill persists strategy memory, workbench data, and field analysis results locally. <br>
Mitigation: Review or delete persisted workbench and memory data when it is no longer needed. <br>


## Reference(s): <br>
- [WQBuddy ClawHub listing](https://clawhub.ai/sebrinass/wqbuddy) <br>
- [wq-buddy npm package](https://www.npmjs.com/package/wq-buddy) <br>
- [wq-buddy project repository](https://github.com/sebrinass/wq-buddy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require local credential, token, database, and OpenClaw configuration files for WorldQuant BRAIN workflows.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
