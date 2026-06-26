## Description: <br>
Publish, submit, and verify local skills across public skill marketplaces, directories, and registries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zjsxply](https://clawhub.ai/user/zjsxply) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release operators use this skill to inspect a local skill folder, prepare marketplace-ready metadata and review bundles, publish to supported directories, and verify public listing outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live publishing can submit skill content and contact details to public marketplaces. <br>
Mitigation: Use dry-run and bundle review first, confirm the intended marketplace and repository scope, and run live submission only with explicit execution flags. <br>
Risk: Skill files may contain secrets, proprietary content, or personal contact details that should not be published. <br>
Mitigation: Review SKILL.md and generated marketplace payloads before submission; remove sensitive content and prefer a public contact address where a marketplace requires email. <br>
Risk: Custom CLI binary flags or marketplace adapters may execute tools outside the normal reviewed path. <br>
Mitigation: Pass custom CLI binary flags only when the executable is trusted and the generated dry-run output matches the intended operation. <br>


## Reference(s): <br>
- [Market Matrix](references/market-matrix.md) <br>
- [Publish Playbook](references/publish-playbook.md) <br>
- [Recon Playbook](references/recon-playbook.md) <br>
- [Verification Playbook](references/verification-playbook.md) <br>
- [ClawHub Skill Listing](https://clawhub.ai/zjsxply/skill-market-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, generated files, JSON bundles, and marketplace payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform live marketplace submissions only when explicitly run with execution flags and required credentials or marketplace inputs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
