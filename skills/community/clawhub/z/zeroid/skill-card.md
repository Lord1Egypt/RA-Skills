## Description: <br>
Identity infrastructure for AI agents: register identities, issue tokens, delegate to sub-agents, revoke credentials, and manage policies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhijitjavelin](https://clawhub.ai/user/abhijitjavelin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate ZeroID identity infrastructure for autonomous agents, including agent registration, OAuth token issuance, delegated access, credential revocation, and policy management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through credential, token, revocation, and policy operations that may affect active identities. <br>
Mitigation: Use the least-privileged ZEROID_API_KEY available and require human review before operations that revoke, delete, or change credential policies. <br>
Risk: Commands depend on the configured ZeroID server and may target production infrastructure if environment variables are pointed there. <br>
Mitigation: Install only when the ZeroID server is trusted, verify ZEROID_BASE_URL before use, and test revoke, delete, and policy changes outside production first. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abhijitjavelin/zeroid) <br>
- [ZeroID homepage](https://github.com/highflame-ai/zeroid) <br>
- [Quickstart Notebook](https://github.com/highflame-ai/zeroid/blob/main/examples/zeroid_quickstart.ipynb) <br>
- [Interactive API docs](https://auth.highflame.ai/docs) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZEROID_API_KEY, ZEROID_BASE_URL, and curl.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
