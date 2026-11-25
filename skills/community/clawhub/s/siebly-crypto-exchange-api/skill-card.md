## Description:

Build, inspect, or modify Node.js and JavaScript cryptocurrency exchange API integrations using Siebly SDKs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harbourlark](https://clawhub.ai/user/harbourlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to build, inspect, and modify Node.js or JavaScript integrations with cryptocurrency exchanges supported by Siebly, including market data, account access, WebSocket workflows, and order-capable integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan is benign with medium confidence but partial because a local path-like reference could not be resolved.

Mitigation: Review the scan guidance and confirm the unresolved reference with the publisher before installation.

Risk: Order-capable exchange integrations can submit transactions that may cause financial loss.

Mitigation: Keep write paths gated behind an explicitly selected execution mode and configured controls; prefer read-only credentials for account queries.

Risk: Exchange API credentials could be exposed if handled carelessly.

Mitigation: Do not request or write secrets into source files, examples, or logs; load credentials through the project's environment configuration.

## Reference(s):

- [Siebly AI coding agent guide](https://siebly.io/ai)
- [Task-focused LLM index](https://siebly.io/llms-tasks.txt)
- [AI Pattern Library](https://siebly.io/ai/patterns)
- [Historical Backfill with Live WebSocket Streams](https://siebly.io/ai/historical-live-data-pipeline)
- [Exchange State Management](https://siebly.io/ai/exchange-state)
- [Order Intent Chasing with Exchange APIs & WebSockets](https://siebly.io/ai/order-intent-chaser)
- [Siebly SDK directory](https://siebly.io/sdk)
- [Siebly examples hub](https://siebly.io/examples)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with JavaScript or TypeScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include exchange-specific integration and safety guidance.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
