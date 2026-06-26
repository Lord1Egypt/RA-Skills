## Description: <br>
Audit a ClawHub skill for security risks BEFORE installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JonathanJing](https://clawhub.ai/user/JonathanJing) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to inspect ClawHub skills before installation, review reported security patterns, and receive an advisory trust score with remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The auditor fetches target skill files and may install Python dependencies during setup. <br>
Mitigation: Run it in an environment where Python package installation and network access are acceptable, and review setup behavior before first use. <br>
Risk: The optional --llm mode can send inspected skill content to Anthropic for analysis. <br>
Mitigation: Use --llm only for skill content that is acceptable to share with that provider. <br>
Risk: Trust scores are advisory and are not proof that another skill is safe. <br>
Mitigation: Use reported findings as a screening aid and manually review flagged files before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JonathanJing/skill-trust-auditor) <br>
- [JonathanJing publisher profile](https://clawhub.ai/user/JonathanJing) <br>
- [ClawHavoc Pattern Reference](references/clawhavoc-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown summary with optional JSON audit report and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Trust scores are advisory and may include exact file and line findings when available.] <br>

## Skill Version(s): <br>
1.1.3 (source: frontmatter, CHANGELOG, skill.json, server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
