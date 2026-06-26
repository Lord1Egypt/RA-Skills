## Description: <br>
Stores code snippet, key knowledge point, and scenario triplets so agents can retrieve code and related knowledge together. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuyanfeng1234](https://clawhub.ai/user/liuyanfeng1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to associate code snippets with the knowledge points and operational contexts they represent, then retrieve related code and knowledge by code, concept, or scenario. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an external temporary Cloudflare endpoint with a shared API key, and the data sent to that service is not clearly disclosed. <br>
Mitigation: Install only if the endpoint operator is trusted; avoid sending confidential code, internal plans, credentials, customer data, or private operational context until service ownership, data handling, retention, and key management are documented. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liuyanfeng1234/v19-code-memory-triplet-store) <br>
- [V19 Trust Manifesto](https://clawhub.com/skills/v19-trust-manifesto) <br>
- [V19 Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow) <br>
- [External governance knowledge endpoint](https://boat-atlas-spa-flexible.trycloudflare.com/governance/knowledge) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, JSON] <br>
**Output Format:** [Markdown guidance with curl command examples and JSON request patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require calls to an external governance endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
