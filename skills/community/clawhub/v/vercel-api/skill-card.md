## Description: <br>
Vercel API integration with managed OAuth for managing projects, deployments, domains, teams, and environment variables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to interact with Vercel through Maton-managed OAuth, including checking deployments, managing projects, configuring domains, handling teams, and updating environment variables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect live Vercel projects, deployments, domains, teams, and environment variables through a connected account. <br>
Mitigation: Use the narrowest practical Vercel connection and approve write actions only after confirming the exact project, deployment, domain, team, or environment variable being changed. <br>
Risk: Multiple Vercel connections can cause requests to target the wrong account. <br>
Mitigation: Specify the intended connection when more than one Vercel account is connected. <br>
Risk: Access depends on Maton brokering Vercel OAuth credentials. <br>
Mitigation: Install the skill only if you trust Maton to broker access to the target Vercel account. <br>


## Reference(s): <br>
- [Vercel REST API Documentation](https://vercel.com/docs/rest-api) <br>
- [Vercel API Reference](https://vercel.com/docs/rest-api/endpoints) <br>
- [Maton](https://maton.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/vercel-api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, API calls] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a connected Vercel OAuth account.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
