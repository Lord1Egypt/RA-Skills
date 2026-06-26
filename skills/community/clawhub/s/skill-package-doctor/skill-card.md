## Description: <br>
Audit Claude, Codex, OpenClaw, and ClawHub skill packages before publishing; produce concrete fix lists, trust scores, and shareable proof cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill to audit local Claude, Codex, OpenClaw, and ClawHub skill packages before marketplace release. It helps produce publish decisions, scores, blocking issues, concrete fixes, changed-file lists, and optional proof-card output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled script can write JSON, Markdown, and SVG reports to caller-supplied output paths. <br>
Mitigation: Run it only against folders intended for audit and choose report output paths deliberately. <br>
Risk: Capability tags include wallet and credential-related labels that the security guidance says appear overbroad for the package behavior. <br>
Mitigation: Do not assume wallet or credential handling is required; review the release metadata and security summary before deploying policy based on those tags. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zack-dev-cm/skill-package-doctor) <br>
- [Publisher profile](https://clawhub.ai/user/zack-dev-cm) <br>
- [source-manifest.json](references/source-manifest.json) <br>
- [Skill homepage](https://clawhub.getgeofix.xyz/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown report with optional JSON, Markdown, and SVG proof-card files from the bundled script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create files at user-selected --json-out, --markdown-out, and --svg-out paths.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
