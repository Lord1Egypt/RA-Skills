## Description: <br>
Run slither static analysis on Solidity contracts. Fast, lightweight security scanner for EVM smart contracts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aviclaw](https://clawhub.ai/user/aviclaw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and smart contract engineers use this skill to run local Slither static analysis on Solidity files or contract directories and generate vulnerability findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external Slither/PyPI package to perform analysis. <br>
Mitigation: Install slither-analyzer in an isolated environment and use a trusted package source. <br>
Risk: The analyzer runs against local contract paths supplied by the user. <br>
Mitigation: Run it only on intended local Solidity files or directories and review the target path before execution. <br>
Risk: The artifact includes an unused detect.md prompt that does not describe the actual Slither-based execution path. <br>
Mitigation: Treat slither-audit.py and the documented Slither workflow as the operative behavior, not the unused prompt file. <br>


## Reference(s): <br>
- [Slither static analyzer](https://github.com/crytic/slither) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, JSON, text, shell commands, analysis] <br>
**Output Format:** [Markdown report by default, with optional JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports local Slither findings for a provided Solidity file or directory.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
