## Description: <br>
Fetches recent Twitter/X activity from AI-domain KOL accounts, identifies high-interest topics, and generates professional internal briefing reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ryder-MHumble](https://clawhub.ai/user/Ryder-MHumble) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, operators, and developers use this skill to monitor selected AI-company, researcher, investor, and influencer accounts on Twitter/X, cluster noteworthy AI topics, and produce Markdown internal reports with strategic analysis and source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports an embedded fallback Twitter API key. <br>
Mitigation: Remove the fallback key before installation and require users to provide scoped credentials through config.json or environment configuration. <br>
Risk: Tweet and topic data may be sent to OpenRouter for opportunity detection and report generation. <br>
Mitigation: Use only data approved for third-party model processing, and configure provider access according to the deployment's data-handling policy. <br>
Risk: The security review notes that the skill writes cached tweet and filtered-topic data under /tmp despite claiming no local files are saved. <br>
Mitigation: Redirect or delete the cache files after execution, and document the temporary-file behavior for users before deployment. <br>


## Reference(s): <br>
- [KOL account list](references/kol_list.json) <br>
- [LLM prompts](references/llm_prompts.md) <br>
- [Internal report template](references/internal_report_template.md) <br>
- [TwitterAPI.io](https://twitterapi.io) <br>
- [OpenRouter API](https://openrouter.ai/api/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown reports and console text, with JSON configuration and intermediate JSON data during execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TwitterAPI.io for tweet retrieval and OpenRouter-hosted models for topic selection and report generation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
