## Description: <br>
You Inc Life Ops is a multi-agent personal life operations system that routes natural-language user needs across 12 role-based agents for wellbeing, productivity, relationships, learning, finance, leisure, and crisis support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zabr1314](https://clawhub.ai/user/zabr1314) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill as a personal life-management assistant that can initialize a local YOU-INC workspace, route conversations to specialized agent personas, and maintain markdown memories for health, emotions, relationships, finances, goals, hobbies, and work habits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can keep persistent memories about sensitive personal domains including health, emotions, relationships, finances, and work habits. <br>
Mitigation: Require explicit user consent before memory writes, narrow or disable memory for sensitive topics, and periodically review or delete stored context files. <br>
Risk: The skill can automatically use dependent skills that access or change private notes, calendars, Apple Health data, and email. <br>
Mitigation: Require confirmation before any health, email, calendar, or Obsidian access and review each dependent skill separately before enabling it. <br>
Risk: The artifact references a hard-coded Obsidian vault path. <br>
Mitigation: Remove the hard-coded vault path and ask the user to provide or confirm their own vault location before Obsidian operations. <br>
Risk: The skill includes crisis and psychological support flows that may be used in high-stakes mental-health situations. <br>
Mitigation: Keep crisis responses focused on immediate safety, provide appropriate professional support resources, and avoid presenting the skill as a replacement for medical or mental-health professionals. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zabr1314/you-inc-life-ops) <br>
- [SKILL.md](SKILL.md) <br>
- [ORCHESTRATOR.md](references/ORCHESTRATOR.md) <br>
- [Crisis escalation protocol](references/PROTOCOLS/危机升级流程.md) <br>
- [Conflict arbitration protocol](references/PROTOCOLS/冲突仲裁规则.md) <br>
- [Health log template](references/CONTEXT-TEMPLATES/健康日志.md) <br>
- [Relationship map template](references/CONTEXT-TEMPLATES/关系图谱.md) <br>
- [Finance snapshot template](references/CONTEXT-TEMPLATES/财务快照.md) <br>
- [Goals and reflection template](references/CONTEXT-TEMPLATES/目标与反思.md) <br>
- [Hobby progress template](references/CONTEXT-TEMPLATES/爱好进展.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Conversational text and markdown workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local YOU-INC markdown context files and memory logs.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
