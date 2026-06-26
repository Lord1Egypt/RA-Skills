## Description: <br>
SkillUp is a cross-platform skill publishing tool for packaging and syncing custom skills to GitHub, Xiaping Skill, OpenClaw CN, and ClawHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjke84](https://clawhub.ai/user/cjke84) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use SkillUp to check, package, redact-scan, and publish custom agent skills across GitHub, Xiaping Skill, OpenClaw CN, and ClawHub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing uses platform tokens and can push skill artifacts to external services. <br>
Mitigation: Use least-privilege tokens, prefer environment variables over committed config files, and run dry-run plus redact-check before publishing. <br>
Risk: Local install and rollback modes can replace local agent skill files. <br>
Mitigation: Use install-local or rollback only after reviewing the target paths and confirming backups are available. <br>
Risk: One OpenClaw status call weakens TLS verification. <br>
Mitigation: Verify OpenClaw endpoints are trusted HTTPS services and review status output before relying on it for release decisions. <br>


## Reference(s): <br>
- [SkillUp on ClawHub](https://clawhub.ai/cjke84/skillup) <br>
- [SkillUp homepage](https://github.com/cjke84/SkillUp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create package archives and publish-result JSON files when the user runs the generated commands.] <br>

## Skill Version(s): <br>
0.1.9 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
