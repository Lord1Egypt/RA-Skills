## Description: <br>
慢病筛查辅助。输入居民健康数据（体征/检验/生活方式/家族史），评估高血压、糖尿病、心脑血管疾病等慢性病风险，给出分级和管理建议（JSON + 自然语言摘要）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Community healthcare workers and public-health staff use this skill to screen resident health data for chronic disease risk, control status, management recommendations, and follow-up frequency. It supports hypertension, diabetes, cardiovascular and cerebrovascular disease, COPD, and chronic kidney disease screening workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send sensitive resident health data to a remote model provider. <br>
Mitigation: Use only with authorization to send the data to the configured provider, manually remove identifiers first, and confirm endpoint, retention, logging, and compliance controls before using real patient or resident data. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON followed by a natural language summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May print to stdout or write results to a file when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
