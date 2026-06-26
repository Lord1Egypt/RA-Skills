## Description: <br>
Find buying-intent leads on Reddit via Brave Search without Reddit account credentials, then score prospects and draft value-first comment structures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[3rdbrain](https://clawhub.ai/user/3rdbrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, growth, and developer-relations teams use this skill to find Reddit discussions that show buying intent, prioritize prospects, and prepare helpful reply structures. It supports manual review workflows rather than automated posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and prospecting queries are sent to Brave Search when BRAVE_API_KEY is configured. <br>
Mitigation: Use only queries appropriate for Brave Search and avoid including confidential customer, account, or internal strategy details. <br>
Risk: Generated comments or post templates may be inaccurate, overly promotional, or misaligned with subreddit rules. <br>
Mitigation: Manually review every generated response for accuracy, disclosure, and subreddit rule compliance before posting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/3rdbrain/reddit-prospecting) <br>
- [Brave Search API](https://api.search.brave.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and console text with structured prospect analysis, scoring summaries, and comment outlines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BRAVE_API_KEY for search; generated comments and prospect scores should be manually reviewed before use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
