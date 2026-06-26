## Description: <br>
Curates persistent memory by filtering what matters, organizing it by function, and pruning stale context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to decide what memory is worth retaining, organize memory files by retrieval function, resolve contradictions, and prune stale context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory may retain sensitive personal, business, health, financial, credential, or token information. <br>
Mitigation: Review what the agent saves, use forget and never-remember controls, and avoid saving sensitive details unless retention is intentional. <br>
Risk: Stale or incorrect memories can mislead future agent responses. <br>
Mitigation: Record dates, source hints, and confidence; prune completed commitments, archive inactive contexts, and keep the newest higher-confidence memory when contradictions appear. <br>


## Reference(s): <br>
- [Remember on ClawHub](https://clawhub.ai/ivangdavila/remember) <br>
- [categories.md](artifact/categories.md) <br>
- [consolidation.md](artifact/consolidation.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with memory file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; produces memory curation, organization, review, and pruning guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
