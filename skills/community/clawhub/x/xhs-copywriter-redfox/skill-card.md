## Description: <br>
Generates Xiaohongshu note copy by querying RedFox trend data, analyzing high-performing notes, and producing publish-ready titles, body text, tags, and source-pattern rationale. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, content operators, and brand teams use this skill to research current Xiaohongshu trends and generate platform-style promotional or creator notes from a chosen topic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a RedFox API key and sends topic queries to the RedFox service. <br>
Mitigation: Use a scoped, revocable REDFOX_API_KEY and avoid submitting confidential topics or client-sensitive prompts. <br>
Risk: Personal writing samples may contain private diaries, unpublished drafts, personal identifiers, or proprietary text. <br>
Mitigation: Provide only short, redacted excerpts when style matching is needed. <br>
Risk: The helper script can create local HTML report files. <br>
Mitigation: Run it from an appropriate working directory and review the output path before using file output options. <br>


## Reference(s): <br>
- [Xiaohongshu Hot Article Data Format](references/xhs_hot_article_format.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/redfox-data/xhs-copywriter-redfox) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with generated titles, body copy, tags, source-pattern rationale, and referenced note summaries; helper script output can also be JSON or HTML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY and may call the RedFox API with topic queries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
