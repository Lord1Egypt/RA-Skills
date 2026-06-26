## Description: <br>
Supports pharmaceutical clinical trial statistics by preparing descriptive statistics, group comparisons, and AI-assisted Markdown interpretation from trial records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and clinical research teams use this skill to summarize grouped clinical trial endpoint data, compare group means, and produce structured JSON plus Markdown analysis notes for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process sensitive clinical trial data and sends trial summaries to an external LLM/API. <br>
Mitigation: Use only data approved for that API, de-identify regulated or confidential trial materials where possible, and confirm organizational approval before processing protected data. <br>
Risk: Broad document parsing for PDFs, legacy Office files, and images can expose the runtime to risky or malformed inputs. <br>
Mitigation: Run converters in a sandboxed environment with file size, runtime, and network limits, and prefer structured JSON inputs when possible. <br>
Risk: AI-generated clinical-trial interpretation may be incomplete or misleading if used as a formal statistical conclusion. <br>
Mitigation: Treat the output as descriptive analysis support and require review by qualified statisticians or clinical reviewers before regulatory, clinical, or business use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-clinical-trial-statistics) <br>
- [Statistical Analysis reference skill](https://agent-skills.md/skills/Jst-Well-Dan/Skill-Box/statistical-analysis) <br>
- [Unisound-LLM publisher profile](https://clawhub.ai/user/unisound-llm) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Analysis, Guidance] <br>
**Output Format:** [UTF-8 JSON containing structured statistics and Markdown natural-language analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an appkey for the configured external medical LLM API; JSON-only inputs do not require optional document parsing tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
