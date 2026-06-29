## Description: <br>
Use when the user asks to cut a release, tag a version, publish a release, or roll up the changelog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[escoffier-labs](https://clawhub.ai/user/escoffier-labs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release maintainers use this skill to turn accumulated merged work into a tagged release with a changelog roll-up, version bump, GitHub release, and draft announcement text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Release automation can push version commits, tags, and GitHub releases that are hard to unwind cleanly. <br>
Mitigation: Run only after confirming a clean default branch, green CI, passing local tests, matching changelog and git history, and explicit release intent. <br>
Risk: Installation may add local command-correction hooks that inspect or rewrite shell commands and store local learning data. <br>
Mitigation: Review the installer and release source before install, avoid curl-to-bash when review is required, and leave telemetry disabled unless explicitly desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/escoffier-labs/skillet-release-cut) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, markdown, text] <br>
**Output Format:** [Markdown with inline shell commands and release text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose repository edits, tags, GitHub release notes, and announcement drafts; social posts remain drafts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
