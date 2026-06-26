## Description: <br>
Search YouTube videos, channels, and trends via the AISA API using queries, filters, and pagination without requiring Google credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and content researchers use this skill to search YouTube SERP results, discover channels and videos, monitor trends, and perform competitor research through the bundled Python client. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an AISA API key and sends user-provided YouTube search queries to api.aisa.one. <br>
Mitigation: Install only when use of AISA_API_KEY and the AISA relay is acceptable; avoid including secrets or private business details in search queries. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/bibaofeng/youtube-search-aisa) <br>
- [AISA YouTube API endpoint](https://api.aisa.one/apis/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses from the bundled Python client] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; search queries are sent to api.aisa.one.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
