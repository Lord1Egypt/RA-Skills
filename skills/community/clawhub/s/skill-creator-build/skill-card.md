## Description: <br>
Build helps an agent generate a customized project-building skill with SKILL.md and references that guide planning, technical decisions, staged implementation, and project review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[balancegsr](https://clawhub.ai/user/balancegsr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and skill authors use Build to create a project-specific agent skill that keeps a build effort organized from intake through delivery. The generated skill can create project memory files, reference guides, and workspace or ZIP packaging for the user's project. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create a new skill directory and project-memory folder in a workspace. <br>
Mitigation: Install it only in a workspace where those files are expected, and review the generated preview and destination path before direct installation. <br>
Risk: Project-memory files may persist and be reloaded by generated skills in later sessions. <br>
Mitigation: Do not put secrets or sensitive credentials in plan.md, decisions.md, or other generated project-memory files. <br>
Risk: Local path detection may select an installation prefix the user did not intend. <br>
Mitigation: Use ZIP delivery when manual inspection or placement is preferred. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/balancegsr/skill-creator-build) <br>
- [README](artifact/README.md) <br>
- [Engineering checklist template](artifact/references/templates/guides/engineering_checklist.md) <br>
- [Full project review guide template](artifact/references/templates/guides/project_review_full.md) <br>
- [Lite project review guide template](artifact/references/templates/guides/project_review_lite.md) <br>
- [Full build skill template](artifact/references/templates/skill/full.md) <br>
- [Lite build skill template](artifact/references/templates/skill/lite.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown skill files, reference files, project-memory files, and optional ZIP packaging guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local files only after user preview and delivery confirmation.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
