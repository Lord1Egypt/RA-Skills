## Description: <br>
Expose a local API service to the public internet via aitun tunnel for external testing and integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ctz168](https://clawhub.ai/user/ctz168) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to expose a locally running REST, GraphQL, gRPC, or HTTP API through an aitun public tunnel for external testing, review, and integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A public tunnel can expose local APIs, secrets, admin routes, debug routes, private data, or unauthenticated write endpoints to the internet. <br>
Mitigation: Use the tunnel only for services intended to be internet-reachable; review exposed routes and add authentication and rate limiting before sharing the public URL. <br>
Risk: Tunnel sessions can leave a local service reachable longer than intended during testing. <br>
Mitigation: Stop the aitun process when testing is complete and avoid exposing private services such as databases or SSH unless that exposure is intentional and protected. <br>


## Reference(s): <br>
- [AiTun homepage](https://aitun.cc) <br>
- [ClawHub skill page](https://clawhub.ai/ctz168/skills/remote-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local service startup examples, tunnel commands, endpoint sharing text, test commands, and cleanup guidance.] <br>

## Skill Version(s): <br>
1.0.6 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
