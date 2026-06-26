## Description: <br>
AI助手帮助备考日语N2和软考架构师，支持智能出题、自动判分、错题记录和个性化学习计划。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[it-worker-club](https://clawhub.ai/user/it-worker-club) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students and self-learners use this skill to practice Japanese N2/N1 and software architect exam questions, receive answer feedback, review wrong answers, and generate study plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on Feishu Bitable-backed study data and is described by security evidence as prototype-quality. <br>
Mitigation: Use it with non-sensitive learning data and review privacy expectations, data retention, and deletion controls before broader deployment. <br>
Risk: Broad activation phrases may trigger study workflows in more situations than intended. <br>
Mitigation: Review triggers before deployment and narrow them if the agent is used in shared or mixed-purpose chat environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/it-worker-club/study-buddy-niu) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill description](artifact/SKILL.md) <br>
- [Batch mode guide](artifact/BATCH_MODE_GUIDE.md) <br>
- [Testing guide](artifact/TESTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown-style chat responses with quiz questions, answer feedback, study plans, and progress summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use Feishu Bitable-backed progress and wrong-answer storage when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
