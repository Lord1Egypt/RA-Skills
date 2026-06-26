## Description: <br>
Stop talking to a robot. Give your OpenClaw agent a soul that truly cares. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yoborlon-alpha](https://clawhub.ai/user/yoborlon-alpha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw developers use Soul Harbor to add bilingual conversational companionship that adapts persona by sentiment, remembers selected personal context locally, and can produce scheduled proactive follow-up messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and reuses sensitive personal and emotional context in local memory. <br>
Mitigation: Use it only when this companion behavior is intentional; avoid medical, financial, crisis, or highly private details unless local persistence is acceptable. <br>
Risk: Proactive messages may later reference remembered moods, relationships, health, work, or date-related facts. <br>
Mitigation: Review or delete the generated local data store when stopping use, and limit access to the stored profile files. <br>
Risk: The artifact includes incomplete OpenClaw integration points for LLM response generation, entity extraction, user enumeration, and proactive message delivery. <br>
Mitigation: Review the integration behavior before deployment and confirm that message sending, memory extraction, retention, and deletion controls meet the intended environment. <br>


## Reference(s): <br>
- [Soul Harbor on ClawHub](https://clawhub.ai/yoborlon-alpha/soul-harbor) <br>
- [yoborlon-alpha Publisher Profile](https://clawhub.ai/user/yoborlon-alpha) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text responses with optional Markdown and inline shell or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate bilingual English or Chinese companion replies and proactive follow-up messages based on local memory.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter and package files report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
