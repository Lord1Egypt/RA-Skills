## Description: <br>
Trump Daily Report tracks Trump-related social posts and major US media coverage, then generates bilingual market analysis reports for morning and evening review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xsqorange](https://clawhub.ai/user/xsqorange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts and agent operators use this skill to collect Trump-related social and media signals, compare them with recent report history, and produce bilingual market reports with source-labeled market data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports are saved locally as report history. <br>
Mitigation: Set memory_path to a dedicated folder with appropriate access controls and review retained report files under organizational data-handling policy. <br>
Risk: Generated reports are sent to a configured Feishu group. <br>
Mitigation: Verify feishu_group_id before scheduled use and test delivery with non-sensitive content before enabling routine report posting. <br>
Risk: The skill may use r.jina.ai or other third-party news fetch paths when collecting source material. <br>
Mitigation: Review organizational policy for third-party fetch services and prefer approved sources when handling sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xsqorange/trump-daily-report) <br>
- [Media sources reference](references/media-sources.md) <br>
- [Truth Social profile](https://truthsocial.com/@realDonaldTrump) <br>
- [X profile](https://x.com/realDonaldTrump) <br>
- [BBC News via Agent Reach](https://r.jina.ai/https://www.bbc.com/news/world/us_and_canada) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, analysis, guidance] <br>
**Output Format:** [Markdown bilingual reports and trend summaries, with source-labeled market data and optional shell commands for fetching or analyzing supporting data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local report history files and sends generated reports to a configured Feishu group when used as described.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
