## Description: <br>
Build high-yield Quizlet study sets, tune Learn and Test sessions, and improve weak cards with spaced repetition diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Students and other Quizlet users use this skill to design focused study sets, choose study modes, plan study sessions, and improve cards that repeatedly fail retention checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores study goals, deadlines, preferences, and weak-card patterns in local notes under ~/quizlet/. <br>
Mitigation: Keep stored notes minimal and avoid passwords, payment information, private identifiers, or unrelated personal data. <br>
Risk: Poorly scoped or overloaded card guidance can lead to misleading confidence or weaker retention. <br>
Mitigation: Use the skill's atomic-card, test-mode, and missed-card rewrite checks before relying on a study set for exam preparation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/quizlet) <br>
- [Skill Homepage](https://clawic.com/skills/quizlet) <br>
- [Setup - Quizlet](setup.md) <br>
- [Quizlet Set Design](set-design.md) <br>
- [Quizlet Study Modes](study-modes.md) <br>
- [Retention Diagnostics for Quizlet](diagnostics.md) <br>
- [Quizlet Import and Cleanup Workflows](imports.md) <br>
- [Memory Template - Quizlet](memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with tables, checklists, templates, and local note structure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local notes under ~/quizlet/; does not make network requests or log in to Quizlet by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
