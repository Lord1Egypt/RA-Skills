## Description: <br>
Recognizes natural-language BI query intent and extracts indicator and dimension information for downstream analytics routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LoveNerverMore](https://clawhub.ai/user/LoveNerverMore) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and BI teams use this skill to route rewritten business questions into data-query, metadata-query, attribution-analysis, or other intent paths, while extracting the metric and dimension data needed by later workflow steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can load credentials from a shared skills .env file. <br>
Mitigation: Install only in a trusted BI environment and keep unrelated secrets out of the shared skills .env file. <br>
Risk: Queries and credentials can be sent to configurable external Gemini-compatible endpoints. <br>
Mitigation: Restrict who can set gemini_api_url, require HTTPS, and allow only approved endpoints. <br>
Risk: The workflow can carry matched_sql or logic_dsl into later SQL-generation stages. <br>
Mitigation: Validate matched_sql and logic_dsl in a separate SQL safety stage before execution. <br>
Risk: Evidence reports an embedded token risk. <br>
Mitigation: Remove or rotate the embedded token before installing the release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LoveNerverMore/recognize-intent) <br>
- [Publisher profile](https://clawhub.ai/user/LoveNerverMore) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Configuration, Shell commands] <br>
**Output Format:** [JSON object or JSON file containing intent, indicator_metric, candidates, mode, success, message, and optional clarification data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May pass through matched_sql from a prior workflow step and may include logic_dsl-enhanced metric data for downstream SQL generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact frontmatter says 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
