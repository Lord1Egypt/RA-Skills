## Description: <br>
RedPincer helps authorized security testers run automated AI/LLM red-team assessments against LLM API endpoints, including prompt injection, jailbreak, data extraction, guardrail bypass, adaptive follow-ups, heatmaps, regression testing, and exportable reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rustyorb](https://clawhub.ai/user/rustyorb) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Security engineers, AI developers, and authorized auditors use this skill to assess LLM endpoints for prompt injection, jailbreak, data extraction, and guardrail-bypass weaknesses, then review results and export findings for remediation tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is dual-use and could be misapplied against endpoints without permission. <br>
Mitigation: Use it only for authorized LLM security testing and confirm written permission for every endpoint before running assessments. <br>
Risk: Prompts, credentials, or reports may expose sensitive data if used with production systems or shared devices. <br>
Mitigation: Use test API keys and non-production data where possible, and avoid storing sensitive prompts, credentials, or reports in localStorage on shared devices. <br>
Risk: Running the companion application requires local Node.js dependencies. <br>
Mitigation: Review the repository and npm dependencies before running npm ci. <br>


## Reference(s): <br>
- [RedPincer ClawHub release](https://clawhub.ai/rustyorb/redpincer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide the agent to generate or export security assessment reports after authorized LLM testing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
