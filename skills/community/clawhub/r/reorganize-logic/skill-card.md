## Description:

Rebuilds a project's architecture, structure, and interface contracts from code when existing documentation is too stale to synchronize, with structural verification and human-reviewed legacy deletion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentjiang06](https://clawhub.ai/user/vincentjiang06)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to re-derive design contracts from an existing codebase when legacy documentation has drifted beyond incremental repair.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad project reading may expose sensitive code or documentation to the agent.

Mitigation: Use the reviewed release and limit the project scope where appropriate.

Risk: Rebuilt contracts or legacy-document changes may misrepresent or discard important behavior.

Mitigation: Run the local verifier, review the new contracts, and personally approve the deletion manifest before deleting or overwriting legacy files.

## Reference(s):

- [ClawHub release: reorganize-logic](https://clawhub.ai/vincentjiang06/skills/reorganize-logic)
- [Rebuild protocol](artifact/references/protocol.md)
- [Contract format](artifact/references/contract-format.md)
- [Verification gate design](artifact/references/gate-design.md)

## Skill Output:

**Output Type(s):** [Files, Guidance, Shell commands]

**Output Format:** [Markdown contracts and deletion manifest with verification results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Architecture, structure, and interface contracts; legacy deletion requires human approval.]

## Skill Version(s):

0.3.4 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
