## Description: <br>
Daily fact extraction from AI agent session history into a persistent learned.md memory file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to turn prior OpenClaw conversations into a searchable local memory of decisions, fixes, configuration changes, and other durable facts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill summarizes local agent session history into persistent memory, which may include secrets, client data, personal information, or confidential project details. <br>
Mitigation: Review session-history sensitivity before enabling scheduled runs, keep the generated memory files local, and periodically inspect or delete memory/.dreams and memory/learned.md. <br>
Risk: Extracted memories can preserve incorrect or low-value facts if the agent accepts noisy conversation content. <br>
Mitigation: Use the documented extraction rules, confidence thresholds, source citations, and budget gate, then review learned.md before relying on the retained facts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zero2ai-hub/skill-dreaming-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and structured JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local extraction input under memory/.dreams, appends learned facts to memory/learned.md, and reports processed sessions, extracted facts, confidence range, and budget remaining.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
