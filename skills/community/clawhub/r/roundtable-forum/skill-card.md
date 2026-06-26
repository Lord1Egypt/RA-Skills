## Description: <br>
Roundtable Forum helps an agent facilitate structured multi-perspective discussions, summarize points of disagreement, and generate ASCII reasoning diagrams and knowledge-network summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangzhixu](https://clawhub.ai/user/zhangzhixu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to run a moderated roundtable over a complex topic, explore competing viewpoints, continue or deepen discussion rounds, invite additional participants, and capture a structured knowledge network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic reminders may add or rely on a Cron entry that is not fully documented in the artifact. <br>
Mitigation: Confirm the exact Cron entry and removal steps before enabling reminders. <br>
Risk: Knowledge-network outputs may preserve sensitive discussion content. <br>
Mitigation: Avoid sensitive topics when outputs will be saved, or review and redact saved Markdown before sharing. <br>
Risk: Documentation references helper files that are not present in the artifact. <br>
Mitigation: Review any added helper files separately before installation or execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangzhixu/roundtable-forum) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with ASCII diagrams and optional configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate knowledge-network Markdown outputs; review saved outputs before sharing sensitive discussion content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
