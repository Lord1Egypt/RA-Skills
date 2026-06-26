## Description: <br>
Configure and verify bearer API key authentication for Remix agent publishing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chuckstock](https://clawhub.ai/user/chuckstock) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent builders use this skill to configure bearer API key authentication for Remix server APIs and verify a key from a server-side runtime before using agent publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Remix bearer API key can grant account or project access if exposed through logs, browser code, or an overprivileged runtime. <br>
Mitigation: Create the least-privileged key available, store it only as a server-side secret, avoid logging it, and verify first with a disposable or test Remix project. <br>


## Reference(s): <br>
- [Remix API keys](https://remix.gg/api-keys) <br>
- [Remix API base URL](https://api.remix.gg) <br>
- [Remix API documentation](https://api.remix.gg/docs) <br>
- [ClawHub skill page](https://clawhub.ai/chuckstock/remix-api-key-auth) <br>
- [Publisher profile](https://clawhub.ai/user/chuckstock) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bearer authorization header guidance, server-side secret storage guidance, verification steps, and troubleshooting checks.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
