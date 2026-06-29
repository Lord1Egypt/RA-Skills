## Description: <br>
Rebuilds a project's design-contract layer from code when documentation has drifted, producing architecture, structure, and interface contracts that are checked by a verifier gate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentjiang06](https://clawhub.ai/user/vincentjiang06) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to replace badly drifted design-contract documentation with fresh architecture, structure, and interface Markdown derived from the current code. It is intended for deliberate rebuilds, not lightweight documentation syncs or implementation changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [Rebuild protocol](references/protocol.md) <br>
- [Contract format](references/contract-format.md) <br>
- [Gate design](references/gate-design.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown files with Mermaid diagrams, interface tables, a deletion manifest, and verifier command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review the deletion manifest before applying changes; the security scan notes that deletion is human-reviewed rather than automatic.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
