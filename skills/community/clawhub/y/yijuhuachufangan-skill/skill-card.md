## Description: <br>
Generates complete Chinese-language proposal documents from a short request, with automatic matching for government, business, and technical scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leslietong2046-ship-it](https://clawhub.ai/user/leslietong2046-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to turn a brief Chinese-language requirement into a structured Markdown proposal for government, business, or technical planning work. The optional CLI can generate the same proposal from the command line and save it as a Markdown file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases may cause the skill to activate for general planning or writing requests. <br>
Mitigation: Install it only when broad proposal-writing behavior is desired, or require explicit invocation in environments where accidental activation would be disruptive. <br>
Risk: Generated proposals may include default metrics, budgets, timelines, or organizational assumptions that are not validated for the user's actual context. <br>
Mitigation: Review generated proposal content before use and replace template defaults with verified project, budget, policy, and stakeholder information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leslietong2046-ship-it/yijuhuachufangan-skill) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>
- [CLI proposal generator](references/yijuhua.py) <br>
- [Government proposal template](templates/gov.md) <br>
- [Business proposal template](templates/biz.md) <br>
- [Technical proposal template](templates/tech.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown proposal document; optional CLI output can be printed to stdout or saved as a Markdown file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language proposal content with scenario-specific templates and optional command-line generation.] <br>

## Skill Version(s): <br>
2.0.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
