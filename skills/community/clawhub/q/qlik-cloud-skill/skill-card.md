## Description: <br>
Qlik Cloud provides agent guidance for operating Qlik Cloud resources, including health checks, search, app management, reloads, natural language analytics queries, automations, AutoML, Qlik Answers, alerts, governance, data files, and lineage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[undsoul](https://clawhub.ai/user/undsoul) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and platform administrators use this skill to inspect and operate Qlik Cloud tenants from an agent, including apps, reloads, users, spaces, analytics queries, automation runs, alerts, and lineage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Qlik tenant credentials that may grant broad access. <br>
Mitigation: Use a least-privilege Qlik API key and avoid storing secrets in shared or committed files. <br>
Risk: The documented workflows include high-impact actions such as deleting apps, triggering or canceling reloads, running automations, and triggering alerts. <br>
Mitigation: Require explicit user confirmation before any destructive, state-changing, or alert-triggering action. <br>
Risk: The artifact references operational scripts that are not present in the submitted artifact. <br>
Mitigation: Verify the scripts from a trusted source before providing Qlik credentials or running operational commands. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; documented scripts return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QLIK_TENANT and QLIK_API_KEY environment variables.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
