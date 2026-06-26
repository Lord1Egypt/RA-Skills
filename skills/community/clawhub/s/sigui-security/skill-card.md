## Description: <br>
AI security oracle for blockchain transactions that evaluates EVM, Starknet, and Aptos transactions with Sigui Protocol before execution and returns ALLOW, BLOCK, or ESCALATE verdicts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ibonon](https://clawhub.ai/user/ibonon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, wallet operators, and autonomous agent builders use this skill to check specific blockchain transactions before submission. It helps classify transaction risk, request deeper analysis for ambiguous cases, and require explicit user confirmation before proceeding after an allow verdict. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can influence blockchain transaction decisions involving wallets, credentials, or funds. <br>
Mitigation: Use a trusted Sigui API endpoint, keep the explicit user-confirmation step, and do not proceed with transactions when the skill blocks, escalates, or errors. <br>
Risk: The skill fetches Python dependencies automatically during installation or first use. <br>
Mitigation: Install in a dedicated trusted Python environment and review the Sigui SDK package before production use. <br>
Risk: Demo mode produces heuristic test output that is not authoritative for real transactions. <br>
Mitigation: Avoid demo mode for real funds and require a configured production Sigui API endpoint for transaction authorization workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ibonon/sigui-security) <br>
- [Publisher profile](https://clawhub.ai/user/ibonon) <br>
- [Sigui project homepage](https://github.com/ibonon/Sigui) <br>
- [sigui-sdk on PyPI](https://pypi.org/project/sigui-sdk/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON evaluation output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces transaction safety verdicts and exits fail-closed when the Sigui API endpoint or confirmation requirements are not satisfied.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence, SKILL.md frontmatter, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
