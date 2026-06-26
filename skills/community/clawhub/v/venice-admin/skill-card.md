## Description: <br>
Venice AI account administration - check balance, view usage history, and manage API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sabrinaaquino](https://clawhub.ai/user/sabrinaaquino) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to inspect Venice AI account balance, usage history, and API-key metadata from an agent workflow. It is intended for accounts where the operator can provide a Venice Admin API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Venice Admin API key with elevated account access. <br>
Mitigation: Use a dedicated key when possible, keep VENICE_API_KEY out of shared shells and logs, and rotate the key if the environment is no longer trusted. <br>
Risk: Balance, usage history, and API-key metadata may expose sensitive account information. <br>
Mitigation: Review JSON or CSV exports before sharing them and avoid writing outputs to shared or untrusted paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sabrinaaquino/venice-admin) <br>
- [Venice AI](https://venice.ai) <br>
- [Venice API documentation](https://docs.venice.ai) <br>
- [PEP 723 inline script metadata](https://peps.python.org/pep-0723/) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, csv, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands; scripts return human-readable status plus JSON or CSV data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and VENICE_API_KEY; usage output can be written to a local file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
