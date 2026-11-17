## Description:

奇门遁甲排盘技能。支持阴阳遁、局数、八门九星八神落宫、断卦解盘自动化分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dglijin-oss](https://clawhub.ai/user/dglijin-oss)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate Qi Men Dun Jia charts for selected dates, cities, and question types, including automated interpretive analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Divination-style outputs and overstated accuracy claims may be mistaken for professional medical, legal, financial, or safety advice.

Mitigation: Use the results only as cultural or entertainment guidance and require independent professional judgment for consequential decisions.

Risk: The bundled backup utility writes under the local OpenClaw skills directory and removes older backup_* folders.

Mitigation: Run scripts/backup.sh only after reviewing its target paths and retention behavior.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dglijin-oss/skills/qimen-pan-skill)
- [奇门遁甲基础知识](references/奇门基础知识.md)
- [Python documentation](https://python.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON chart output, with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can emit Chinese-language chart details, interpretive analysis, and optional JSON from local Python scripts.]

## Skill Version(s):

3.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
