## Description: <br>
Web Search Hub helps agents search DuckDuckGo for web pages, news, images, and videos with filters and text, Markdown, JSON, or file outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anisafifi](https://clawhub.ai/user/anisafifi) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to gather current web, news, image, and video search results for research, fact-checking, market monitoring, and visual-resource discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Returned web links and snippets may be untrusted, outdated, or misleading. <br>
Mitigation: Verify important claims and links against trusted sources before relying on the results. <br>
Risk: The output option can write search results to a local path selected by the user. <br>
Mitigation: Use intended file paths, avoid overwriting important files, and review saved results before reuse. <br>
Risk: The skill depends on installing the duckduckgo-search package. <br>
Mitigation: Install dependencies from trusted sources, preferably inside a virtual environment. <br>


## Reference(s): <br>
- [Web Search Hub on ClawHub](https://clawhub.ai/anisafifi/web-search-hub) <br>
- [OpenClawCLI](https://clawhub.ai/) <br>
- [duckduckgo-search Python package](https://pypi.org/project/duckduckgo-search/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files, shell commands, guidance] <br>
**Output Format:** [Plain text, Markdown, or JSON search results; optionally written to a local file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are returned from DuckDuckGo web, news, image, or video searches with options for result count, time range, region, safe search, and media filters.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
