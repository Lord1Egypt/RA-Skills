## Description: <br>
A comprehensive tool for creating, documenting, wrapping, and quality-checking professional-grade skills with standardized templates and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[variyaone](https://clawhub.ai/user/variyaone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to scaffold new skills, wrap existing tools, generate documentation, check skill structure, package releases, and install skills into supported agent environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run system package installation commands for dependencies. <br>
Mitigation: Inspect the target skill's _meta.json requires.bins entries and review requested packages before running install-deps. <br>
Risk: The skill can persist files into a local OpenClaw skill installation. <br>
Mitigation: Review generated skill files before using install --openclaw and verify the destination directory after installation. <br>
Risk: Generated or wrapped skills may inherit unsafe behavior from third-party scripts or binaries. <br>
Mitigation: Run a security review and quality check on wrapped tools and generated skill directories before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/variyaone/skill-forge-va) <br>
- [README.md](artifact/README.md) <br>
- [references/examples.md](artifact/references/examples.md) <br>
- [hooks/openclaw/HOOK.md](artifact/hooks/openclaw/HOOK.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated files, JSON metadata, scripts, shell commands, and checklist-style review output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or copy skill directories, templates, wrapper scripts, metadata files, examples, changelogs, and OpenClaw installation artifacts.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata, _meta.json, and CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
