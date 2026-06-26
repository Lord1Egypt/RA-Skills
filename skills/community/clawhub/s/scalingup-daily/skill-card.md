## Description: <br>
Generates structured Markdown reports on search, advertising, and recommendation model Scaling Up developments, then publishes them to IMA and Tencent Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fandywang87](https://clawhub.ai/user/fandywang87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to track recent papers, technical articles, open source projects, and conference activity in recommendation, search, and advertising model scaling. It produces a verified-link report and can publish the Markdown output to configured knowledge and document platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic publishing can send generated reports to IMA and Tencent Docs using stored cloud credentials. <br>
Mitigation: Enable automation only after confirming the target IMA knowledge-base ID, Tencent Docs registration, and token ownership, and review the first report before publishing. <br>
Risk: Credential files and API responses may expose sensitive IMA or Tencent access details if logs or local files are mishandled. <br>
Mitigation: Restrict credential-file permissions, avoid sharing terminal logs or raw API responses, and rotate credentials if exposure is suspected. <br>
Risk: The IMA upload flow depends on an external COS upload helper from an installed IMA skill. <br>
Mitigation: Use only a trusted installed IMA skill and verify the helper path before running uploads. <br>


## Reference(s): <br>
- [Known papers reference](references/known_papers.md) <br>
- [Daily report template](templates/daily_report_template.md) <br>
- [ClawHub skill page](https://clawhub.ai/fandywang87/scalingup-daily) <br>
- [Publisher profile](https://clawhub.ai/user/fandywang87) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with citation index and optional JSON search results from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires web search, WeChat article search, IMA credentials, Tencent Docs MCP access, Node.js, Python 3, jq, and configured platform tokens for publishing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
