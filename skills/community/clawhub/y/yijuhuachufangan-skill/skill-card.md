## Description:

Generates complete Chinese-language proposal documents from a short request, automatically selecting government, business, or technical plan structures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leslietong2046-ship-it](https://clawhub.ai/user/leslietong2046-ship-it)

### License/Terms of Use:

MIT

## Use Case:

External users, employees, and developers can use this skill to draft structured Chinese proposal documents for government, business, or technical scenarios from a brief prompt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases such as requests to write a plan can cause the skill to produce a full structured proposal.

Mitigation: Use the skill where automatic proposal drafting is intended, and review the generated document before relying on it.

Risk: Generated government, sensor, data-sharing, budget, KPI, or timeline claims may be inaccurate or unsuitable for a real project.

Mitigation: Have a qualified reviewer validate claims, numbers, responsibilities, and compliance-sensitive content before using the proposal in real work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leslietong2046-ship-it/skills/yijuhuachufangan-skill)
- [README](README.md)
- [CLI proposal generator](references/yijuhua.py)
- [Government proposal template](templates/gov.md)
- [Business proposal template](templates/biz.md)
- [Technical proposal template](templates/tech.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown proposal documents with optional CLI output and file generation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language proposal drafts may include generated budgets, timelines, KPIs, and implementation steps that require human review.]

## Skill Version(s):

2.0.4 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
