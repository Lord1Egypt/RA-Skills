## Description: <br>
Test WebSocket connections, message flows, and real-time features. Connect to endpoints, send/receive messages, test reconnection logic, measure latency, validate message schemas, and load test concurrent connections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to test, debug, and diagnose WebSocket endpoints for real-time applications, including connection setup, message flow, reconnection behavior, latency, schema validation, and concurrent load testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Concurrent load testing can disrupt or overload WebSocket services when run against systems without authorization or with excessive connection counts. <br>
Mitigation: Run load tests only against systems you own or are explicitly authorized to test, start with lower connection counts and shorter durations, and monitor the target while testing. <br>
Risk: Authenticated WebSocket tests can expose broad or production credentials if reused directly in examples. <br>
Mitigation: Use test credentials or narrowly scoped tokens for authenticated endpoints. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command examples, test scripts, diagnostic notes, and summarized test results for WebSocket endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
