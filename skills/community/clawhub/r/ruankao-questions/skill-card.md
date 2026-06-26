## Description: <br>
搜索和获取中国软考高级科目历年真题、模拟题、论文范文和案例分析备考材料。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wujiaming88](https://clawhub.ai/user/wujiaming88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Ruankao advanced exam candidates and study assistants use this skill to find past papers, simulated practice questions, answers, explanations, essay prompts, and case-analysis guidance for the five advanced exam subjects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Chinese study trigger phrases may activate the skill for queries that are not actually about Ruankao advanced exams. <br>
Mitigation: Confirm the user query is about Ruankao advanced exam preparation before using the skill's public lookup workflow. <br>
Risk: The skill may run read-only GitHub CLI API commands or fetch public web pages during lookup. <br>
Mitigation: Review fetched sources before relying on results, and avoid providing private or sensitive query material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wujiaming88/ruankao-questions) <br>
- [Data source configuration](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with exam questions, answers, explanations, source notes, and optional shell commands for public data lookup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are filtered by exam subject, year range, knowledge area, paper type, and content type when provided.] <br>

## Skill Version(s): <br>
3.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
