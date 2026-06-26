## Description: <br>
Tork Guardian is an AI governance and safety layer for OpenClaw agents that redacts sensitive data, enforces tool and network policies, scans skills for vulnerabilities, and generates compliance audit trails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[torkjacobs](https://clawhub.ai/user/torkjacobs) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security teams use Tork Guardian to add policy enforcement, PII redaction, network controls, vulnerability scanning, and compliance receipts to OpenClaw agent deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Governed prompt content and security telemetry may be routed to Tork's service under the user's Tork API key. <br>
Mitigation: Review Tork's retention and processing terms before use with sensitive or regulated data. <br>
Risk: Cloud service unavailability may affect governance reliability because the evidence guidance identifies current fail-open behavior. <br>
Mitigation: Use strict or custom network policies and avoid relying on this release where governance must block when the service is unavailable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/torkjacobs/tork-guardian) <br>
- [README](README.md) <br>
- [Quick Start](docs/QUICK-START.md) <br>
- [Network Security](docs/NETWORK-SECURITY.md) <br>
- [Security Scanner](docs/SCANNER.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with TypeScript snippets, JSON examples, shell commands, and configuration objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce governance decisions, redacted text, compliance receipts, scanner reports, and badge markdown through the documented SDK and CLI.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
