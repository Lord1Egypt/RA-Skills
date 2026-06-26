## Description: <br>
Unbounce API integration with managed OAuth for building and managing landing pages, tracking leads, and analyzing conversion data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to access Unbounce through Maton-managed OAuth, inspect accounts and pages, manage OAuth connections, track leads, and prepare approved create, update, or delete API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Maton API key and managed OAuth to access an Unbounce account, including landing page and lead data. <br>
Mitigation: Keep MATON_API_KEY private, install only when Maton is trusted to broker the intended Unbounce account, and review Maton's handling of lead data before use. <br>
Risk: Create, update, or delete API calls can change Unbounce connections, pages, leads, or related account resources. <br>
Mitigation: Confirm the exact account, page, lead, connection, and intended effect with the user before any write or delete action. <br>


## Reference(s): <br>
- [ClawHub Unbounce skill page](https://clawhub.ai/byungkyu/unbounce) <br>
- [Maton](https://maton.ai) <br>
- [Unbounce API Documentation](https://developer.unbounce.com/api_reference/) <br>
- [Maton Community](https://discord.com/invite/dBfFAcefs2) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, and HTTP endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses MATON_API_KEY and Maton-managed OAuth; write and delete actions require explicit user approval before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
