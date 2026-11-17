## Description:

Quantum Bridge helps agents transpile quantum circuits between Qiskit OpenQASM and OriginIR, validate OriginIR, run IBC multi-agent consensus, and submit circuits to Quantum Bridge simulator or hardware backends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adjusternwachukwu-bot](https://clawhub.ai/user/adjusternwachukwu-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert quantum circuit formats, validate OriginIR, run consensus workflows, check available quantum backends, and submit jobs through the Quantum Bridge API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled CLI can send API keys and local circuit files to the endpoint configured by QUANTUM_BRIDGE_URL.

Mitigation: Use a protected environment variable or secret store for QUANTUM_BRIDGE_KEY, confirm the endpoint before running the CLI, and avoid submitting sensitive circuit or JSON files unless upload to the Quantum Bridge service is intended.

Risk: The security verdict is suspicious for releases that handle proprietary circuits, research data, or paid API credits.

Mitigation: Review the skill before installing in environments that handle proprietary circuits, research data, or paid API credits.

## Reference(s):

- [Quantum Bridge API](https://quantum-api.gpupulse.dev/api/v1)
- [Quantum Bridge service](https://quantum-api.gpupulse.dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with API examples, shell commands, and JSON response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Quantum Bridge API responses such as transpiled circuit text, validation results, consensus groups, task IDs, backend lists, credit balances, and measurement counts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
