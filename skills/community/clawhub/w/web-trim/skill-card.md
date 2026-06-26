## Description: <br>
Fetches a webpage, removes extraneous content, and returns a concise summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tfops22](https://clawhub.ai/user/tfops22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to summarize public, non-sensitive webpages after trimming common page clutter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private, internal, or credential-bearing URLs may expose sensitive content when fetched and summarized. <br>
Mitigation: Use the skill for public or non-sensitive webpages and avoid submitting URLs that require credentials or contain confidential information. <br>
Risk: Broad trigger wording may activate on general research or summarization requests. <br>
Mitigation: Confirm the intended URL and summarization scope before fetching page content. <br>
Risk: Long webpages may be truncated before summarization, which can omit important details. <br>
Mitigation: Review the source page directly before relying on the summary for important decisions. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/tfops22/web-trim) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Concise Markdown summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries are capped at about 500 words and may be based on truncated page content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
