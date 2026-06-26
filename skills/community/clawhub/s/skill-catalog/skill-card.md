## Description: <br>
Auto-scan all installed skills, generate a categorized INDEX.md, and keep it in sync via git hooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenwang-dev](https://clawhub.ai/user/kenwang-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain a searchable Markdown inventory of installed skills. It helps agents and humans find skill paths and trigger descriptions without manually crawling every SKILL.md file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hook installer can overwrite existing pre-commit and post-merge hooks and persistently change repository behavior. <br>
Mitigation: Inspect existing .git/hooks/pre-commit and .git/hooks/post-merge files before running install-hooks.sh, and merge any existing hook behavior manually. <br>
Risk: The installed pre-commit hook can regenerate and stage skills/INDEX.md automatically when skills change. <br>
Mitigation: Prefer running register.sh manually for lower-risk use, and review the generated INDEX.md diff before committing. <br>


## Reference(s): <br>
- [Skill Index on ClawHub](https://clawhub.ai/kenwang-dev/skill-catalog) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown index file with shell command usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates skills/INDEX.md and can install Git hooks that keep the index updated during commit and pull workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
