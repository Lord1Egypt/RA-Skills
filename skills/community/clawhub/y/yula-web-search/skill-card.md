## Description: <br>
Yula's custom web search helper uses public anonymous search services through curl and Python HTML parsing to retrieve current web results, extract selected page content, and summarize it for the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjzhb](https://clawhub.ai/user/wjzhb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill when an agent needs current web information, news, prices, product availability, specific page extraction, or Chinese-language web research without configuring a search API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User queries and selected page URLs may be sent to public search engines and websites. <br>
Mitigation: Use only when that disclosure is acceptable, and avoid searching for sensitive, confidential, or regulated data. <br>
Risk: The artifact includes shell and Python snippets that interpolate query text into commands. <br>
Mitigation: Pass query text as an argument or through stdin, and review generated commands before execution with untrusted input. <br>
Risk: Broad activation can route requests to live web search when a narrower tool would be more appropriate. <br>
Mitigation: Prefer specialized tools for weather, local file search, or already-provided context, and confirm web access is needed before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wjzhb/yula-web-search) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/wjzhb) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with summarized search results, source URLs, and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and python3; extracts content from selected public web pages and should keep total extracted text bounded.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
