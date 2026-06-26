## Description: <br>
Audit, debug, and clean up the OpenClaw skills you already have installed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris-openclaw](https://clawhub.ai/user/chris-openclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Skill Doctor to audit installed skills for trigger conflicts, security review prompts, stale versions, and ambiguous skill selection. It helps them interpret local audit results and choose concrete cleanup actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects local installed-skill folders and may surface snippets from user files. <br>
Mitigation: Run it only on skill directories the user intends to audit, and share only the findings and snippets needed to explain concrete issues. <br>
Risk: Security findings are heuristic review prompts, not proof of malicious behavior. <br>
Mitigation: Frame flagged items as evidence to review, cite the exact file and line, and avoid declaring a skill malicious from a scanner hit alone. <br>
Risk: Optional stale-version checks may invoke the clawhub CLI when available. <br>
Mitigation: Treat remote version checks as optional and continue with local conflict and security analysis when the CLI is unavailable. <br>


## Reference(s): <br>
- [Skill Doctor release page](https://clawhub.ai/chris-openclaw/skill-doctor-audit) <br>
- [Publisher profile](https://clawhub.ai/user/chris-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON output from the bundled audit tool] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local audit output may include file paths, line numbers, snippets, severity labels, version status, and ambiguity warnings.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, changelog, evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
