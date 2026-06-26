## Description: <br>
Story generation pipeline skill for multi-episode continuous generation, graph management, AI quality checks, and human confirmation before continuation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hexidyg](https://clawhub.ai/user/hexidyg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators and developers use Shorts Builder to manage serialized story generation workflows, including episode prompts, quality review, story graph state, pause/resume, and human approval between episodes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted pipeline ID can cause local graph storage to write outside the intended graph folder. <br>
Mitigation: Use only skill-generated pipeline IDs until the package validates pipeline_id against a safe identifier pattern and resolves graph paths under data/graphs. <br>
Risk: Story pipeline state and generated content may include private or sensitive story material. <br>
Mitigation: Avoid sensitive private material and review stored pipeline data before sharing or deploying the skill. <br>
Risk: Stored story graph or pipeline data may be difficult to recover if modified or deleted unintentionally. <br>
Mitigation: Add deletion confirmation or recovery before operational use, and keep backups of important pipeline state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hexidyg/shorts-builder) <br>
- [Skill source](artifact/SKILL.md) <br>
- [AI quality review template](artifact/templates/review_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown prompts and previews with JSON status and review objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces story episode generation prompts, review prompts, pipeline status, and graph-backed continuity guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
