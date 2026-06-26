## Description: <br>
A Tavily-powered AI search and insight skill that searches the web, summarizes results, analyzes topic sentiment, and extracts webpage content into concise briefs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[airoom-ai](https://clawhub.ai/user/airoom-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Tavily-backed web searches, gather source summaries, extract webpage content, and produce lightweight sentiment or intelligence briefs from public web inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, webpage URLs, and extraction targets are sent to Tavily for processing. <br>
Mitigation: Avoid secrets, private internal URLs, pre-signed links, and confidential research topics unless external Tavily processing is acceptable. <br>


## Reference(s): <br>
- [Tavily](https://tavily.com) <br>
- [ClawHub skill page](https://clawhub.ai/airoom-ai/tavily-search-up) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown-like terminal text with source links, summaries, extracted content, and sentiment labels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and TAVILY_API_KEY; sends user-provided queries and URLs to Tavily.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
