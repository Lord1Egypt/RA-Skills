## Description: <br>
X2C Distribution and Wallet API - publish video to the X2C platform and manage assets including balance, claim, swap, withdrawal, and transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patches429](https://clawhub.ai/user/patches429) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to publish video projects to X2C, upload media through presigned URLs, check review status, and manage X2C wallet actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to publish content or add episodes to X2C projects. <br>
Mitigation: Require manual confirmation before publish or add-episode requests, and verify title, category, cover URL, video URLs, and project ID before execution. <br>
Risk: The skill can direct wallet actions including claim, swap, and USDC withdrawal. <br>
Mitigation: Require explicit human approval for every wallet action, including amount, asset, destination address, and expected result. <br>
Risk: The skill depends on API keys stored in environment variables or credential files. <br>
Mitigation: Use least-privileged X2C API keys, protect credential files, and avoid exposing keys in prompts, logs, or command output. <br>
Risk: The skill can use a configurable API endpoint. <br>
Mitigation: Verify X2C_API_BASE_URL before use and do not send credentials to untrusted endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/patches429/storyclaw-x2c-publish) <br>
- [Publisher profile](https://clawhub.ai/user/patches429) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an X2C API key and may use USER_ID-specific credential files.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
