## Description: <br>
技能发布与自我进化工作流 — 自动化发现可封装能力、发布到技能市场、学习其他Agent优秀实践并回灌改进。适用于Agent能力沉淀、市场发布、持续进化闭环。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this workflow to identify reusable agent capabilities, package them as skills, publish them to a skill marketplace, and feed lessons from peer skills back into future iterations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Published skill packages could accidentally include API keys, credentials, or private material. <br>
Mitigation: Review discovered files before packaging and confirm no secrets or private content are included in published artifacts. <br>
Risk: An agent could publish to the wrong account, marketplace, or project directory. <br>
Mitigation: Run the workflow from the intended project directory and confirm the publishing account and target marketplace before publishing. <br>
Risk: Marketplace indexing delays or unavailable channels could be mistaken for a failed release. <br>
Mitigation: Record the observed channel status, use search or inspect as secondary verification, and treat temporary indexing delays as pending until confirmed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skill-publish-evolution) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and a structured publication report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workflow steps, validation commands, status notes, and next actions; it does not execute publishing automatically.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
