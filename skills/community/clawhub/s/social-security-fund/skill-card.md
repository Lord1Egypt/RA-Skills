## Description: <br>
Social Security Fund helps users estimate Chinese social security and housing fund contributions, pensions, take-home pay, employer costs, and official query channels for major Chinese cities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[testmtcode](https://clawhub.ai/user/testmtcode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and employees use this skill for local estimates of Chinese social security, housing fund, take-home pay, employer cost, and pension planning, plus official-channel lookup guidance. It is not a live account-access tool; query-style outputs are simulated unless the user follows official channels. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake simulated query outputs or 2024 reference rates for authoritative account or policy data. <br>
Mitigation: Treat calculations as estimates and verify balances, eligibility, rates, and pension amounts through the official local social security or housing fund channels listed by the skill. <br>
Risk: Real ID card or housing fund account numbers entered as command-line arguments may be exposed through shell history or process listings. <br>
Mitigation: Use guide mode or placeholder identifiers unless necessary, and avoid passing sensitive personal identifiers on the command line. <br>
Risk: Python dependencies and local scripts execute in the user's environment. <br>
Mitigation: Install dependencies in an isolated Python environment and review the skill before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/testmtcode/social-security-fund) <br>
- [Publisher profile](https://clawhub.ai/user/testmtcode) <br>
- [README](artifact/README.md) <br>
- [Skill instructions and official-channel list](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text, with optional JSON from the included scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local estimates and simulated query outputs; official channels are required for authoritative account data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
