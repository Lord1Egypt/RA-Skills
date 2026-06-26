## Description: <br>
Maintains an llm-wiki knowledge base by importing new sources, answering wiki-backed questions, running health checks, and updating related wiki pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiehanlin](https://clawhub.ai/user/xiehanlin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-base maintainers use this skill to keep a local llm-wiki repository organized, ingest new material, answer questions from existing wiki pages, and repair common wiki health issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can copy local files and update wiki content, which could expose or alter private or business information. <br>
Mitigation: Use it only with a trusted wiki directory, confirm before copying local files or applying repairs, and keep the wiki in version control or backed up. <br>
Risk: The skill may fetch network articles through a third-party service. <br>
Mitigation: Confirm that URLs and fetched content are public or approved before ingestion. <br>
Risk: The skill may run a local lint script during health checks. <br>
Mitigation: Review the script path and ask the agent to confirm before running lint.sh. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiehanlin/wiki-maintainer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with wiki links, file paths, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update wiki pages, index entries, and log records when the agent is operating on a trusted local wiki.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
