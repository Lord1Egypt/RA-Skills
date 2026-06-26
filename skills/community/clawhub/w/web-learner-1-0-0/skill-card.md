## Description: <br>
Enables an agent to search, fetch, and browse the web for current information, then summarize findings in structured Chinese with sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[332054781](https://clawhub.ai/user/332054781) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill when an agent needs current or source-backed information, such as news, weather, events, documents, and topic research beyond training data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Web searches, fetched URLs, or browser activity may be sent to external services. <br>
Mitigation: Use the skill only with public or non-sensitive topics, and avoid confidential prompts, private URLs, and sensitive account pages. <br>
Risk: Web results may be incomplete, unavailable, blocked, or misleading. <br>
Mitigation: Summarize with visible source attribution, state retrieval failures, and use alternate public sources when the first source cannot be accessed. <br>


## Reference(s): <br>
- [Web Learner reference resources](artifact/references/resources.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Chinese Markdown summaries with source notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes concise bullet points, source attribution, and clear failure notes when web access is unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
