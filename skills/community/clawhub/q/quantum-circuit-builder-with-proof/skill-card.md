## Description:

Builds quantum circuits from templates, provider snippets, or Lean source and produces Lean-kernel-backed proof certificates, diagrams, provider exports, and simulation receipts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and auditors use this skill to build, inspect, certify, verify, export, and simulate quantum circuits when a circuit needs replayable proof evidence or audit-ready artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Quantum circuits, claims, certificates, and submitted Lean source may be sent to AgentPMT.

Mitigation: Submit only content approved for that data boundary, and do not include secrets or proprietary source unless organizational policy allows it.

Risk: Companion setup instructions may use unpinned npx install commands.

Mitigation: Review or pin companion setup skills and install commands before use.

Risk: Submitted Lean source runs as trusted code in the service environment rather than in an untrusted-code sandbox.

Mitigation: Use only internally trusted Lean source and review receipt fields that describe execution mode and isolation.

Risk: Circuit inspection, visualization, provider export, and simulation outputs can be mistaken for proof or hardware execution.

Mitigation: Treat only the qpcert and its stated claim ledger as proof evidence, and independently replay certificates received from other parties.

## Reference(s):

- [Action schema](artifact/schema.md)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/quantum-circuit-builder-with-proof)
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/quantum-circuit-builder-with-proof)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-oriented tool call guidance with inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May refer to generated files, proof certificates, circuit diagrams, provider exports, simulation receipts, and background task results.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
