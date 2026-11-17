## Description:

Tesla China helps agents configure and run Node.js commands for China-region Tesla vehicle queries and remote controls through the Tesla Fleet API via tesla.dhuar.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mywind2020](https://clawhub.ai/user/mywind2020)

### License/Terms of Use:

MIT-0

## Use Case:

External Tesla owners in China and their agents use this skill to list vehicles, read vehicle data, and issue supported remote commands such as wake, lock, trunk, lighting, horn, HVAC, charge-port, and remote sound actions.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill routes Tesla API keys, VINs, telemetry, and vehicle command traffic through tesla.dhuar.com, a third-party service with under-disclosed high-impact access.

Mitigation: Install only if the user intentionally trusts tesla.dhuar.com with vehicle access, or prefer a version that uses official Tesla authorization directly and clearly documents the proxy operator and safety controls.

Risk: The skill can issue physical vehicle commands, including lock, trunk, horn, HVAC, charge-port, lighting, and remote sound actions.

Mitigation: Confirm vehicle identity and surroundings before issuing commands, start with non-actuating checks such as list or vehicle data, and use disruptive commands only in safe and lawful conditions.

Risk: The apiKey is stored in ~/.tesla_cn.json and may also be exposed through shell history if passed on the command line.

Mitigation: Treat the apiKey as a sensitive vehicle-control secret, restrict local file permissions manually, and avoid placing the key in command-line history or shared logs.

## Reference(s):

- [Tesla China ClawHub skill page](https://clawhub.ai/mywind2020/skills/tesla-cn)
- [Tesla China API key service](https://tesla.dhuar.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell command examples; bundled scripts print JSON or service response text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18 or newer and a Tesla China apiKey stored in ~/.tesla_cn.json or supplied during initialization.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
