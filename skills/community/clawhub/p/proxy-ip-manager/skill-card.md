## Description: <br>
Kuaidaili Proxy IP Manager helps Kuaidaili users configure API credentials, retrieve proxy IPs, inspect order status, check expiry, evaluate IP health, tune concurrency, and review usage statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kuaidaili-ai](https://clawhub.ai/user/kuaidaili-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Kuaidaili customers and developers use this skill to manage proxy account configuration, obtain proxy endpoints, monitor expiry and health, and choose safer concurrency settings for proxy workloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Kuaidaili API secrets and proxy credentials, and terminal output from proxy retrieval may contain usable proxy usernames and passwords. <br>
Mitigation: Install only when the publisher and Kuaidaili account workflow are trusted, protect or remove the local configuration file, and treat proxy retrieval output as secret. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kuaidaili-ai/proxy-ip-manager) <br>
- [Kuaidaili API response reference](references/api_response.md) <br>
- [Proxy health scoring rules](references/scoring_rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with command examples and JSON script results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include proxy endpoints, usernames, passwords, account status, expiry data, health scores, and usage statistics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
