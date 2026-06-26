## Description: <br>
A CISSP exam preparation quiz API that delivers randomized questions, tracks session progress, and evaluates answers in real-time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cybersecurity professionals, training organizations, and developers use this skill to start CISSP quiz sessions, submit answers, and review score and domain performance data through the CISSPly API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill calls a remote ToolWeb.in service. <br>
Mitigation: Install only if you trust the ToolWeb.in service, use pseudonymous session IDs, and avoid sending personal information. <br>
Risk: The agent-facing API includes an admin question-reload endpoint that may change the live question bank. <br>
Mitigation: Do not allow an agent to call /api/admin/reload unless you intentionally have admin authority and understand the operational impact. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-cissply) <br>
- [CISSPly API Route](https://api.toolweb.in/tools/cissply) <br>
- [CISSPly API Docs](https://api.toolweb.in:8175/docs) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown with JSON examples and cURL commands; API responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The remote API returns quiz sessions, submitted-answer evaluations, category performance, service health, and admin reload status.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
