## Description: <br>
Zzz4ai Search Engine helps agents route Chinese web, academic, news, and video search requests across six public search engines without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bingshangfei](https://clawhub.ai/user/bingshangfei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill when an agent needs to search Chinese-language web content, Bilibili or Toutiao results, academic papers, or video tutorials. The skill selects suitable public search engines, builds search URLs, filters duplicate results, and returns a source-linked report. <br>

### Deployment Geography for Use: <br>
Global; optimized for Chinese-region search providers. <br>

## Known Risks and Mitigations: <br>
Risk: Private or sensitive search terms may be sent to public Chinese search providers. <br>
Mitigation: Avoid private or sensitive queries unless the user is comfortable sending them to those providers; for privacy, political, medical, or financial searches, confirm scope before searching. <br>
Risk: Broad trigger terms may cause an agent to invoke the skill for routine informational requests more often than intended. <br>
Mitigation: Narrow trigger criteria or require a search-specific user intent when deploying the skill in agents with frequent general-question traffic. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bingshangfei/zzz4ai-search-engine) <br>
- [Advanced search guide](references/advanced-search.md) <br>
- [Bing search tips](https://cn.bing.com/tips) <br>
- [360 Search help](https://www.so.com/help.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown search report with source labels and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search URLs are generated from configured public engine templates; no API key is required.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release, metadata.json, CHANGELOG; released 2026-05-18) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
