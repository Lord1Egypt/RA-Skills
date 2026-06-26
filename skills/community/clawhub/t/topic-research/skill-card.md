## Description: <br>
Run a second-hop deep research pass through the Tavily CLI after an initial scan, then normalize the result into a local `research.md` contract. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abigale-cyber](https://clawhub.ai/user/abigale-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to turn a selected topic or prior news scan into a cited research report with writing recommendations, evidence notes, and saved raw source data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A source_file excerpt can be sent to Tavily as part of the research prompt. <br>
Mitigation: Use only intended, non-sensitive input files and exclude secrets, credentials, personal data, and unrelated project content. <br>
Risk: Raw research results are retained locally and may include third-party content or sensitive context from the request. <br>
Mitigation: Review and scrub the raw JSON before sharing it, publishing it, or committing it to a repository. <br>
Risk: The workflow depends on installing and authenticating the Tavily CLI. <br>
Mitigation: Verify the Tavily installer source and confirm the CLI is installed, logged in, and acceptable for the environment before running the skill. <br>


## Reference(s): <br>
- [ClawHub Topic Research release page](https://clawhub.ai/abigale-cyber/topic-research) <br>
- [Tavily CLI installer](https://cli.tavily.com/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, json, guidance] <br>
**Output Format:** [Markdown research report and raw JSON source archive] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a normalized research report under content-production/inbox/ and raw Tavily results under content-production/inbox/raw/research/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
