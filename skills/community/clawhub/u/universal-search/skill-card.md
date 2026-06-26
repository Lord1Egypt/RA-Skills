## Description: <br>
全网搜索接口 - 孙永乐开发的高质量全网搜索API，返回结构化结果，带可信度评分和交叉验证。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cattei](https://clawhub.ai/user/cattei) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to query a web-search API from an agent workflow and receive summarized answers, source links, and credibility-scored cross-checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User queries are sent to an external Coze-hosted service. <br>
Mitigation: Use only trusted queries and avoid submitting secrets, private business data, or personal data. <br>
Risk: The skill includes bundled endpoint and bearer-token defaults. <br>
Mitigation: Configure a trusted UNIVERSAL_SEARCH_URL and UNIVERSAL_SEARCH_TOKEN before deployment instead of relying on bundled defaults. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cattei/universal-search) <br>
- [Search service homepage](https://49srjp57sf.coze.site) <br>
- [Search API endpoint](https://49srjp57sf.coze.site/run) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Formatted text summary or JSON returned by a command-line Python script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes answer summaries, details with source attribution, source lists, and credibility scores when returned by the external service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
