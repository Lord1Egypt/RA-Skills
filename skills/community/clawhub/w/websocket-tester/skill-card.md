## Description:

Test WebSocket connections, message flows, and real-time features. Connect to endpoints, send/receive messages, test reconnection logic, measure latency, validate message schemas, and load test concurrent connections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to test, debug, and load test WebSocket endpoints for real-time applications such as chat, game servers, IoT, streaming APIs, and live update systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ready-to-run examples include unsafe command construction.

Mitigation: Review and adapt commands before execution, and pass host values as validated data rather than interpolating them into code.

Risk: The command examples use unpinned runtime tooling.

Mitigation: Pin or preinstall trusted WebSocket testing tools instead of relying on unpinned npx execution.

Risk: The load-test example can create concurrent traffic against a target service.

Mitigation: Run load tests only against systems you own or are explicitly authorized to test, preferably in staging and with lower initial concurrency.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/websocket-tester)
- [Publisher profile](https://clawhub.ai/user/charlie-morrison)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces connection tests, message validation examples, reconnection checks, latency measurements, load-test scripts, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
