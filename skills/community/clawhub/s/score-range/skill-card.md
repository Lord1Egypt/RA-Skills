## Description: <br>
A GaoKao score and rank lookup assistant that extracts province, year, subject category, score, and rank from a user request, then queries Tencent GaoKao score-range data through its bundled Python script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhl-det](https://clawhub.ai/user/jhl-det) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, families, and education advisors can use this skill to look up provincial GaoKao ranking information by score, estimate a score range from a provincial rank, or request a score-by-score ranking table for supported Chinese provinces and subject categories. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Lookup parameters such as province, year, subject category, score, and rank are sent to Tencent's GaoKao service when the skill is used. <br>
Mitigation: Use the skill only when users are comfortable sharing those lookup parameters with Tencent, and avoid entering unnecessary personal information. <br>
Risk: Admissions ranking data can be incomplete, unavailable, or different from official provincial sources. <br>
Mitigation: Treat results as lookup assistance and verify important admissions decisions against official provincial examination authority data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jhl-det/skills/score-range) <br>
- [Tencent GaoKao score-range data service](https://gaokao.search.qq.com/skills_data) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON] <br>
**Output Format:** [Concise natural-language answer with optional script command and JSON-derived lookup results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script accepts province, year, subject category, score, and rank parameters and prints JSON lookup results.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
