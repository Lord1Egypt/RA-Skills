## Description: <br>
Verifies AI agent trust scores and reputation via Towel Protocol for trust checks, reputation lookups, credential imports, and trust-tier display in multi-agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leo-guinan](https://clawhub.ai/user/leo-guinan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to check whether an AI agent has a Towel trust record before relying on its output, and to surface trust tiers in multi-agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled shell scripts can use an authenticated GitHub account to create a private repository and maintain a persistent inter-agent channel. <br>
Mitigation: Review the scripts and intended GitHub organization before execution; run only when repository creation and persistent channel setup are desired. <br>
Risk: Handshake seeds and trust-channel material may be committed to the created repository. <br>
Mitigation: Limit repository access, inspect committed handshake material, and rotate exposed seeds if the workflow was run unintentionally. <br>
Risk: Git remotes may embed GitHub access tokens after the setup script runs. <br>
Mitigation: Inspect git remotes after execution and rotate any exposed GitHub credentials. <br>
Risk: API downtime or missing records can produce an unknown verification state. <br>
Mitigation: Treat unknown, missing, or unreachable Towel records as unverified and require local allowlists or human review before relying on the agent output. <br>


## Reference(s): <br>
- [Towel Protocol](https://towel.metaspn.network) <br>
- [Towel Protocol Spec](https://towel.metaspn.network/spec) <br>
- [Verified List](https://towel.metaspn.network/list) <br>
- [Live API List Endpoint](https://towel.metaspn.network/api/v1/list) <br>
- [ClawHub Skill Page](https://clawhub.ai/leo-guinan/towel-protocol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with API examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public API calls for reputation lookup and optional local shell commands for trust-channel workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
