## Description: <br>
Query Runcloud servers, databases, web apps, services, cronjobs, deployments, and health via the Runcloud API v3. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neshable](https://clawhub.ai/user/neshable) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Runcloud-managed servers, web apps, databases, cron jobs, deployments, services, SSL certificates, domains, and health data. It can also guide explicitly confirmed operational actions such as deployments, cron tests, service restarts, and SSL changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide production-impacting server actions, including deployments, cron tests, service restarts, and SSL changes. <br>
Mitigation: Use a least-privileged Runcloud token and require explicit operator confirmation before running any production-impacting action. <br>
Risk: The Runcloud API token can grant broad workspace access. <br>
Mitigation: Store RUNCLOUD_API_TOKEN securely, avoid exposing it in logs or shared transcripts, and rotate or revoke it if disclosure is suspected. <br>
Risk: The security summary flags the release for review because some operational actions are described as safe or non-destructive. <br>
Mitigation: Review generated commands before execution, especially for production servers, and confirm the intended server, web app, service, cron job, or SSL target ID. <br>


## Reference(s): <br>
- [Runcloud Skill on ClawHub](https://clawhub.ai/neshable/runcloud) <br>
- [Runcloud API v3 Documentation](https://runcloud.io/docs/api/v3/doc-625011) <br>
- [Runcloud API v3 Base URL](https://manage.runcloud.io/api/v3) <br>
- [Runcloud API v2 Fallback Base URL](https://manage.runcloud.io/api/v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and jq command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq and the RUNCLOUD_API_TOKEN environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
