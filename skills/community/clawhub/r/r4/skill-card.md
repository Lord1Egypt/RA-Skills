## Description: <br>
Access and manage credentials, secrets, and domain registrations using the R4 platform with injected environment variables and API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukezirngibl](https://clawhub.ai/user/lukezirngibl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to retrieve project secrets, inject credentials into commands, and manage domain registration and DNS operations through R4. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad access to vault secrets. <br>
Mitigation: Use only with an R4 vault and domain account the user is comfortable exposing to the agent, and prefer scoped or temporary secrets. <br>
Risk: Commands may inject secrets into process environments or reveal secret values. <br>
Mitigation: Require manual confirmation before listing secrets, retrieving secret values, or running commands with injected secrets. <br>
Risk: The skill can purchase domains and change DNS records. <br>
Mitigation: Require manual confirmation before purchasing domains or modifying DNS records. <br>


## Reference(s): <br>
- [R4 API Documentation](https://r4.dev/docs/api-reference) <br>
- [ClawHub R4 Skill Page](https://clawhub.ai/lukezirngibl/r4) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that expose or inject secrets and API calls that purchase domains or modify DNS records.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
