## Description: <br>
SEEM is an episodic memory skill for storing and retrieving structured multi-turn conversation memories with fact graphs, PPR retrieval, hybrid dense and sparse retrieval, dynamic memory integration, and Lite/Pro/Max recall modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryantoleco](https://clawhub.ai/user/ryantoleco) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use SEEM to add persistent episodic memory, structured fact extraction, entity-centric retrieval, and configurable recall depth to multi-turn conversation agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores user-provided memories locally, which can retain sensitive conversation content after the original interaction. <br>
Mitigation: Avoid storing secrets or regulated data unless local retention is acceptable, and clear the local data directory when retained memory is no longer needed. <br>
Risk: The skill sends text to configured LLM and embedding providers. <br>
Mitigation: Use dedicated API keys, set explicit LLM_BASE_URL and MM_ENCODER_BASE_URL values, and confirm the configured providers are acceptable for the data being processed. <br>


## Reference(s): <br>
- [ClawHub SEEM Skill Page](https://clawhub.ai/ryantoleco/seem-skill) <br>
- [Default LLM API Endpoint](https://api.deepseek.com) <br>
- [Default Embedding API Endpoint](https://api.siliconflow.cn/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, code, shell commands, configuration, guidance] <br>
**Output Format:** [Python objects, JSON-like recall results, CLI text, Markdown guidance, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recall output varies by Lite, Pro, or Max mode and may include memories, facts, raw chunks, and backfilled context.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
