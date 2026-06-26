## Description: <br>
Twitter/X intelligence toolkit: analyze users, tweets, trends, communities, and networks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wxtsky](https://clawhub.ai/user/wxtsky) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use readx to analyze Twitter/X users, tweets, trends, communities, and networks, then turn retrieved data into ranked comparisons, derived metrics, and actionable takeaways. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a readx API key, and setup can expose or store that credential. <br>
Mitigation: Use an environment variable or secure config, avoid sharing MCP config files or screenshots containing the key, and rotate the key if it is exposed. <br>
Risk: Broad or parallel Twitter/X analyses may consume readx API credits and send queries to readx.cc. <br>
Mitigation: Install only if you trust readx.cc with the intended Twitter/X data queries, check credit balance before large analyses, and scope requests to the user's actual need. <br>


## Reference(s): <br>
- [readx ClawHub page](https://clawhub.ai/wxtsky/readx) <br>
- [readx service](https://readx.cc) <br>
- [readx API documentation](https://readx.cc/api-docs.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with tables, bullet lists, and inline shell or JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include derived metrics, ranked comparisons, and key takeaways based on available Twitter/X data.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
