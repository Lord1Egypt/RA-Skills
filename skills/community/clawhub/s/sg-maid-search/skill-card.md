## Description: <br>
Search and match available domestic maids from Sunrise Link's database in Singapore, with guided requirements gathering and structured candidate filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meikidd](https://clawhub.ai/user/meikidd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employers in Singapore use this skill to search, filter, and shortlist available domestic maid candidates by budget, skills, nationality, language, religion, age, and Singapore experience. The agent can ask guided questions, run a structured search, and present candidate summaries with links to Sunrise Link profiles. <br>

### Deployment Geography for Use: <br>
Singapore <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for and displays sensitive hiring attributes such as nationality, religion, age, salary, and care needs. <br>
Mitigation: Use these filters only when lawful, necessary, and appropriate for the hiring context; avoid collecting preferences the user says do not matter. <br>
Risk: Candidate profile links lead to external Sunrise Link pages that may expose more personal information than the API response. <br>
Mitigation: Open only official Sunrise Link profile links and avoid copying unrelated private details into the agent conversation. <br>
Risk: Search results come from a live external API and may change over time. <br>
Mitigation: Treat results as search assistance and confirm availability, interviews, and hiring steps through Sunrise Link's official platform. <br>


## Reference(s): <br>
- [Field Guide: Sunrise Link Maid Search](references/field_guide.md) <br>
- [Sunrise Link](https://www.sunriselink.sg) <br>
- [ClawHub Skill Page](https://clawhub.ai/meikidd/sg-maid-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JSON tool input and JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries the Sunrise Link public API and returns candidate attributes, work history, skills evaluation, and profile URLs; the API response excludes candidate names and contact details.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
