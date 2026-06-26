## Description: <br>
Standardizes a five-stage search workflow for query analysis, search execution, result processing, content extraction, and structured report output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earthwalking](https://clawhub.ai/user/earthwalking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to run repeatable searches for academic research, current information, deeper research, and fact checking. It produces structured Markdown reports with summaries, key results, source URLs, and related links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may be sent to Tavily or other external search services. <br>
Mitigation: Use the skill only for queries appropriate to external services and configure secrets through an approved secret mechanism. <br>
Risk: The release was flagged for review because it includes a bundled fallback Tavily API key. <br>
Mitigation: Remove or disable the fallback credential and provide a user-owned TAVILY_API_KEY before running the script. <br>
Risk: Broad keyword activation can trigger searches unexpectedly. <br>
Mitigation: Narrow activation to explicit search-workflow requests before installing it in an agent environment. <br>


## Reference(s): <br>
- [Search Workflow on ClawHub](https://clawhub.ai/earthwalking/search-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report and command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a local timestamped Markdown report when the bundled script runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
