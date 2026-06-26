## Description: <br>
Search the web using SerpAPI with customizable engines (Google, Google AI Mode, Bing, etc.). Use when user needs web search results via SerpAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lsl001006](https://clawhub.ai/user/lsl001006) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run web searches through SerpAPI when a task needs current search results from supported engines. It is useful for retrieving text search-result blocks after the user or environment provides a SerpAPI key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to SerpAPI and may expose confidential or sensitive query content. <br>
Mitigation: Avoid searching secrets, credentials, private customer data, or confidential internal material through this skill. <br>
Risk: The skill depends on a SerpAPI API key and the third-party serpapi Python package. <br>
Mitigation: Provide the key through SERPAPI_API_KEY instead of editing source files, and review or pin the dependency in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lsl001006/web-search-with-serpapi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text search-result blocks returned from SerpAPI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SERPAPI_API_KEY and the serpapi Python package.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
