## Description: <br>
Call RouteMesh's unified JSON-RPC endpoint for EVM chain IDs using a helper script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kermankohli](https://clawhub.ai/user/kermankohli) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to make RouteMesh JSON-RPC calls for EVM chain data, debug RPC responses, and exercise chain or method routing through RouteMesh. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaged skill references a RouteMesh helper script that is not included. <br>
Mitigation: Verify the helper script separately before installing or running the skill. <br>
Risk: RouteMesh API keys may be exposed through logs, shared terminal output, issues, or commits. <br>
Mitigation: Use a scoped or low-value ROUTEMESH_API_KEY and keep it out of logs and shared artifacts. <br>
Risk: The optional --url setting can redirect requests to unintended RPC endpoints. <br>
Mitigation: Set --url only to endpoints the user intentionally trusts. <br>


## Reference(s): <br>
- [RouteMesh](https://routeme.sh) <br>
- [RouteMesh RPC endpoint](https://lb.routeme.sh) <br>
- [ClawHub skill page](https://clawhub.ai/kermankohli/routemesh-crypto-rpc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-RPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference ROUTEMESH_API_KEY and RouteMesh JSON-RPC request parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
