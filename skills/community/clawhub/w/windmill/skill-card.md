## Description: <br>
Build automation workflows and internal tools with Windmill's code-first platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation engineers use this skill as concise reference guidance when creating Windmill scripts, flows, schedules, secrets, self-hosted deployments, and webhook-triggered workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Windmill workflows, scripts, schedules, secrets, or webhook logic may be incorrect or unsafe for production if applied without review. <br>
Mitigation: Review and test generated Windmill assets before production use, including input schemas, schedules, concurrency behavior, secret handling, and webhook authentication. <br>
Risk: Webhook-triggered workflows can expose unauthenticated entry points if generated logic omits token validation or proxy controls. <br>
Mitigation: Require explicit token validation in script logic or enforce authentication through a reverse proxy before exposing webhook URLs. <br>
Risk: Plaintext variables or hardcoded paths can leak sensitive data or reduce portability across Windmill workspaces. <br>
Mitigation: Use Windmill secrets for sensitive values and resource lookup helpers such as wmill.get_resource() for workspace-portable configuration. <br>


## Reference(s): <br>
- [ClawHub Windmill skill page](https://clawhub.ai/ivangdavila/windmill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline code references and implementation notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no executable code is included in the skill artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
