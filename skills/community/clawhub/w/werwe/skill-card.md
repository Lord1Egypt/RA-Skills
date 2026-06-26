## Description: <br>
Search X (Twitter) posts using the xAI API for tweets, current social posts, and topic-specific discussion on X. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[github2cao](https://clawhub.ai/user/github2cao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search public X/Twitter posts through xAI, apply handle and date filters, and return summarized results with citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User search queries are sent to xAI for processing. <br>
Mitigation: Use only an XAI_API_KEY you are comfortable using, and avoid secrets, private personal data, or confidential business topics in queries. <br>
Risk: Search results may reflect incomplete, misleading, or rapidly changing social media posts. <br>
Mitigation: Review cited X posts before relying on the output for decisions or publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/github2cao/werwe) <br>
- [Publisher profile](https://clawhub.ai/user/github2cao) <br>
- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search) <br>
- [xAI Console](https://console.x.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search response with summary text, citations, status, search count, and token usage; agents may present the result as Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and XAI_API_KEY. Supports handle allowlists, handle exclusions, date ranges, and optional image or video understanding.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
