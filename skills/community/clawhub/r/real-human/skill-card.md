## Description: <br>
真实的人类 helps an agent recognize, analyze, and model human individuals for user profiling, personality analysis, behavioral pattern analysis, and personalized interaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wasinc](https://clawhub.ai/user/wasinc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide an agent in building and updating persistent human profile notes for personalization. It is intended for scenarios such as user modeling, understanding a person, personality analysis, and behavioral pattern analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to build persistent personal profiles that can include sensitive emotional, behavioral, relationship, and psychological inferences. <br>
Mitigation: Require explicit user opt-in before profiling, store only user-approved non-sensitive preferences by default, and treat emotional distress and psychological inferences as sensitive. <br>
Risk: Persistent profile files can become inaccurate, overbroad, or difficult for users to control over time. <br>
Mitigation: Provide clear ways for users to inspect, correct, export, and fully delete profile and memory files, and periodically confirm model accuracy with the user. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/wasinc/real-human) <br>
- [信息提取方法](references/extraction-methods.md) <br>
- [人类建模理论框架](references/modeling-framework.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance, profile templates, and structured personal-model notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to create or update persistent human-models/*.md, private profile notes, and relationships.json files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
