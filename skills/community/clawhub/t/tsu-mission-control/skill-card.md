## Description: <br>
Integrate with Mission Control dashboard to report task progress, publish documents to the Library, request approvals, and submit project requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[louisval1](https://clawhub.ai/user/louisval1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect OpenClaw agents to a Mission Control dashboard for task progress reporting, review submission, approvals, project requests, document publishing, and cost reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent hooks and broad automatic reporting can send document content, file paths, error context, model/provider data, and cost telemetry to Mission Control. <br>
Mitigation: Use the skill only in a trusted local or private environment and review what agents will report before connecting it to real work. <br>
Risk: Default access controls may be insecure for exposed deployments. <br>
Mitigation: Enable AUTH_MODE=local with a strong LOCAL_AUTH_TOKEN, set a non-placeholder HOOK_SECRET, restrict CORS_ORIGIN, and avoid exposing Docker ports publicly. <br>
Risk: Library renderer/XSS findings are relevant when untrusted agent or user content appears in the dashboard. <br>
Mitigation: Fix and validate the renderer issues before allowing untrusted content in the dashboard. <br>


## Reference(s): <br>
- [Mission Control on ClawHub](https://clawhub.ai/louisval1/tsu-mission-control) <br>
- [README](README.md) <br>
- [Getting Started](docs/GETTING-STARTED.md) <br>
- [API Reference](docs/API-REFERENCE.md) <br>
- [Hook Events](docs/HOOK-EVENTS.md) <br>
- [Library Guide](docs/LIBRARY-GUIDE.md) <br>
- [Docker Deployment Guide](docs/DOCKER.md) <br>
- [Troubleshooting](docs/TROUBLESHOOTING.md) <br>
- [Changelog](docs/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON payload examples, shell commands, and HTTP endpoint descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing workflow instructions for reporting status, reviews, approvals, project requests, library publications, dispatch polling, and session cost data.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
