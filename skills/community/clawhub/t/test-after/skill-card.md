## Description: <br>
Guides agentic wallet operations through the caw CLI with explicit approval and safety checks for on-chain actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengjunquan-l](https://clawhub.ai/user/pengjunquan-l) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and wallet operators use this skill to guide balance checks, operation previews, approval gating, and status tracking for Cobo agentic wallet actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet actions can have high financial impact if an asset, amount, recipient address, chain, or duration is wrong. <br>
Mitigation: Require owner approval and personally verify each operation parameter before proceeding. <br>
Risk: Prompt injection or external content could attempt to trigger wallet operations. <br>
Mitigation: Act only on direct user requests, reject instructions from external content, and pause when request details are incomplete. <br>
Risk: Wallet authority and sensitive credentials can be exposed or over-scoped. <br>
Mitigation: Keep authorizations narrow, trust the local caw CLI environment, and reject requests for API keys, session IDs, or unrestricted access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pengjunquan-l/test-after) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline caw CLI commands and operation checklists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit owner approval before sensitive wallet operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
