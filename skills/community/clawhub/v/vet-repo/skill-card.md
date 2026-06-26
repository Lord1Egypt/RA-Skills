## Description: <br>
Scan repository agent configuration files for known malicious patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itsnishi](https://clawhub.ai/user/itsnishi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill before trusting a cloned repository or after changes to agent configuration files. It runs a local scanner and reports suspicious agent-level patterns in Claude, MCP, VS Code, Cursor, and related configuration files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The normal scanner path reviews local repository files, so sensitive private repositories may produce local findings that include paths or matched snippets. <br>
Mitigation: Run the scanner only in a trusted local environment and handle generated reports according to the repository's confidentiality requirements. <br>
Risk: The bundled shared module contains a package-registry verification helper that could contact npm or PyPI if invoked separately. <br>
Mitigation: Use the documented vet-repo scanner path for local-only review, or apply network controls before invoking registry verification helpers. <br>


## Reference(s): <br>
- [Vet Repo on ClawHub](https://clawhub.ai/itsnishi/vet-repo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style structured security report printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are grouped by severity with actionable recommendations.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
