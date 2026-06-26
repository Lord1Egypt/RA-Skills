## Description: <br>
智能需求解读技能，通过多级分类和案例匹配帮助用户准确表达需求，并提供标准化交付物清单。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samwang-001](https://clawhub.ai/user/samwang-001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, and AI users use this skill to clarify vague or complex requirements through classification, case matching, structured interview questions, and standardized deliverable checklists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requirement text may include secrets or highly confidential details, and the interpreter keeps a capped in-memory history during its process lifetime. <br>
Mitigation: Avoid entering secrets, credentials, or highly confidential details; restart the process to clear short-lived in-memory history before switching contexts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samwang-001/requirement-interpreter) <br>
- [Requirement Patterns](references/requirement_patterns.md) <br>
- [Requirement Completeness Checklist](assets/checklists/requirement_completeness_checklist.md) <br>
- [AI Communication Checklist](assets/checklists/ai_communication_checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown-style analysis with command-line text output and structured checklist content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local requirement text analysis with classification, confidence, similar cases, interview questions, and deliverable checklist recommendations.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
