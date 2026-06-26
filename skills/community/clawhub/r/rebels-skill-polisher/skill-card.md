## Description: <br>
Polishes standalone skills and multi-skill bundles for ClawHub readability without sacrificing LLM effectiveness, including dependency mapping and regression checking for bundles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[99rebels](https://clawhub.ai/user/99rebels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to improve ClawHub-facing skill documentation for standalone skills or bundles while preserving behavior, security notes, and cross-skill contracts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose changes to SKILL.md and reference files that affect agent behavior if approved without review. <br>
Mitigation: Review the proposed SKILL.md changes, reference files, and audit report before approving any overwrite. <br>
Risk: Target skills may contain credential or token setup documentation that should be preserved only when legitimately required. <br>
Mitigation: Do not provide secrets to the polisher, and verify that credential documentation is preserved rather than broadened or exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/99rebels/rebels-skill-polisher) <br>
- [Audit Guide](references/audit-guide.md) <br>
- [Bundle Rules](references/bundle-rules.md) <br>
- [Polishing Rules](references/rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown files, reference material, and audit reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user approval before overwriting originals.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
