## Description: <br>
Realtime Web Search helps agents perform Baidu-backed live web search and fact-checking with fallback routes and traceable result metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangziiiiii](https://clawhub.ai/user/wangziiiiii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they need current web results, Chinese web evidence, or cross-source verification through Baidu-backed search and summary routes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Baidu using BAIDU_API_KEY and may expose sensitive query text to a third-party service. <br>
Mitigation: Avoid secrets and private data in queries, and use a limited-scope Baidu key appropriate for the intended environment. <br>
Risk: The script prints parsed request bodies, so query text may appear in local logs. <br>
Mitigation: Run it only in trusted environments and avoid submitting confidential query text. <br>
Risk: Endpoint override variables can redirect requests and credentials away from the default Baidu endpoints. <br>
Mitigation: Set BAIDU_WEB_SEARCH_ENDPOINT, BAIDU_CHAT_SEARCH_ENDPOINT, and BAIDU_SUMMARY_ENDPOINT only to trusted Baidu-compatible endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangziiiiii/realtime-web-search) <br>
- [Baidu Qianfan web_search endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search) <br>
- [Baidu Qianfan chat search endpoint](https://qianfan.baidubce.com/v2/ai_search/chat/completions) <br>
- [Baidu Qianfan web_summary endpoint](https://qianfan.baidubce.com/v2/ai_search/web_summary) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [JSON arrays or structured error text, with shell command examples in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Result records may include source, source_endpoint, request_id, answer, title, url, content, and date fields depending on the Baidu route response.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
