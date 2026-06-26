## Description: <br>
Convert files and URLs to structured text using the TokenFlow API with agent-side per-filetype configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kolemaravilla](https://clawhub.ai/user/kolemaravilla) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use TokenFlow to turn supported attachments and pasted URLs into structured text before downstream AI analysis, summarization, or extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Supported attachments, pasted URLs, and optional sign-in credentials are sent to TokenFlow's remote service for processing. <br>
Mitigation: Install only when remote processing is acceptable, avoid private or internal URLs, and prefer an existing API key over entering passwords on the command line. <br>
Risk: Sensitive file types may be converted automatically if default configuration is left unchanged. <br>
Mitigation: Review config.json before use and set askEachTime=true or action=skip for sensitive file types. <br>
Risk: Quota, size, unsupported-format, or service failures can prevent conversion. <br>
Mitigation: Use the configured fallback behavior to keep the original file available and report quota or conversion failures to the user. <br>


## Reference(s): <br>
- [ClawHub TokenFlow release page](https://clawhub.ai/kolemaravilla/tokenflow) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/kolemaravilla) <br>
- [TokenFlow service](https://tokenflow.ironlion.cc) <br>
- [TokenFlow API service](https://tokenflow.fly.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or JSON-derived text returned from TokenFlow API calls, plus concise agent-facing configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOKENFLOW_API_KEY and network access; conversion can fall back to the original file when configured or when quota, size, format, or service errors occur.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
