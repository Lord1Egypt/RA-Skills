## Description:

Prove that exact file bytes existed at a point in time with Verifyum, anchored on Solana Mainnet without uploading the file, and check Verifyum proofs. No account or key. An anchor is a permanent public transaction, so anchor only when the user asks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisenseapi](https://clawhub.ai/user/aisenseapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can create a timestamped proof for a specific local file or commitment, track its status, and verify a public proof. The skill also explains how to configure the hosted and local Verifyum MCP servers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A proof anchor is a permanent public Solana transaction and cannot be withdrawn.

Mitigation: Create an anchor only when the user asks for a proof of that specific file or record, and explain that the record is public and permanent.

Risk: A broadly allowed local directory could expose files beyond those intended for this workflow.

Mitigation: Limit VERIFYUM_MCP_ALLOWED_DIRS to the folder containing the intended files.

Risk: The security review covers the skill instructions but not the unbundled server implementations or their privacy guarantees.

Mitigation: Review the pinned npm package before running the local server.

## Reference(s):

- [Verifyum agent guide](https://verifyum.com/agents)
- [Verifyum agent API documentation](https://verifyum.com/docs/agent-api.md)
- [ClawHub skill page](https://clawhub.ai/aisenseapi/skills/verifyum-proofs)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Natural language with shell commands and proof status or verification details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When creating a proof, includes the public proof details and the path to the private draft that must be kept with the original file.]

## Skill Version(s):

0.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
