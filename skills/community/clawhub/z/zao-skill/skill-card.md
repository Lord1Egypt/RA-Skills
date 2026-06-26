## Description: <br>
Create, design, review, and self-improve agent skills following best practices; use when the user asks to create, write, edit, improve, review, or package a skill; also use when describing a new capability that should be turned into a skill; or when asking about skill design and structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sensenkawa](https://clawhub.ai/user/sensenkawa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent-builders use this skill to design, draft, validate, package, and improve AI agent skills with structured workflows and verification gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search and comparison workflows may read local installed skill metadata or fetch third-party SKILL.md files from the web. <br>
Mitigation: Opt into search only when appropriate, and review imported references as untrusted evidence before incorporating them. <br>
Risk: Skill-building guidance can introduce incorrect or misleading workflows into generated skills. <br>
Mitigation: Use the skill's validation and human review gates before deploying or publishing generated skill content. <br>
Risk: Packaging may publish unintended contents if the release archive is not inspected. <br>
Mitigation: Run validation and check package contents before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sensenkawa/zao-skill) <br>
- [README](README.md) <br>
- [Design Gate](references/design-gate.md) <br>
- [Search Compare](references/search-compare.md) <br>
- [Skill Evolution](references/skill-evolution.md) <br>
- [Verification Gate](references/verification-gate.md) <br>
- [GitHub releases](https://github.com/Sensenkawa/zao-skill/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with checklists, file paths, code edits, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or revise skill files and packaging artifacts when the user asks for implementation.] <br>

## Skill Version(s): <br>
0.8.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
