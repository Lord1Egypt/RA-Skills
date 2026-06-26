## Description: <br>
Skywork Search lets an agent search the web for real-time information through the Skywork Search API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gxcun17](https://clawhub.ai/user/gxcun17) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, employees, and external users can use this skill when an agent needs current web information, recent facts, statistics, source URLs, or research material for downstream writing and analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Skywork as an external web-search provider and may include sensitive user or business information. <br>
Mitigation: Do not include secrets, confidential business data, or sensitive personal information in search queries unless that disclosure is acceptable. <br>
Risk: The skill depends on a Skywork API key for authenticated API access. <br>
Mitigation: Store SKYWORK_API_KEY carefully and avoid printing it in shared terminals, logs, screenshots, or public configuration. <br>
Risk: Search result files are written to a temporary directory and may contain sensitive query text or result snippets. <br>
Mitigation: Delete temporary result files after sensitive searches. <br>


## Reference(s): <br>
- [Skywork API Key Setup Guide](references/apikey-fetch.md) <br>
- [Skywork](https://skywork.ai) <br>
- [Skywork Search ClawHub Page](https://clawhub.ai/gxcun17/skywork-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and text files containing source URLs and snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts one to three search queries per invocation; each query uses a 30-second timeout and writes results to temporary text files.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
