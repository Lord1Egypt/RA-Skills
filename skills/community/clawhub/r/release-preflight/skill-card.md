## Description: <br>
Pre-release safety and scope checker for skills, repos, and export bundles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lethehades](https://clawhub.ai/user/lethehades) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release maintainers use this skill before publishing or sharing a skill folder, repository, or release bundle to check for private artifacts, overscoped publish surfaces, local identity leakage, missing release basics, and export-safety risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may include local paths or filenames from the scanned target. <br>
Mitigation: Review any report before sharing it and run the skill only on the specific skill, repository, or bundle intended for publication. <br>


## Reference(s): <br>
- [Release Preflight on ClawHub](https://clawhub.ai/lethehades/release-preflight) <br>
- [Rules](references/rules.md) <br>
- [Report Format](references/report-format.md) <br>
- [Target Types](references/target-types.md) <br>
- [Export Safety](references/export-safety.md) <br>
- [Release Minimal](references/release-minimal.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional plain-text preflight reports and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports can include local paths or filenames from the scanned target.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
