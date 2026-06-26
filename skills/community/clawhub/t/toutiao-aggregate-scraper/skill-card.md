## Description: <br>
今日头条数据查询助手，用于查询文章、视频、用户和评论数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[new-ironman](https://clawhub.ai/user/new-ironman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Media, content, and operations teams use this skill to look up Toutiao articles, videos, users, and comments through MaxHub APIs and summarize results for monitoring or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Toutiao-related queries and the MaxHub API key are sent to www.aconfig.cn. <br>
Mitigation: Use only in trusted environments, configure MAXHUB_API_KEY as a sensitive secret, and avoid exposing key values in prompts, logs, or output. <br>
Risk: Security evidence notes under-disclosed cross-platform fallback instructions and broad automatic query routing. <br>
Mitigation: Review fallback behavior before deployment and restrict use to documented Toutiao and MaxHub endpoints unless additional routes are explicitly approved. <br>
Risk: The skill can support bulk profiling or personal-data collection if used without proper authorization. <br>
Mitigation: Use proportionate, authorized queries only, and apply privacy, compliance, and data-retention controls before operational use. <br>


## Reference(s): <br>
- [MaxHub API website](https://www.aconfig.cn) <br>
- [Content and User API Reference](references/api-content-user.md) <br>
- [Parameter Mappings](references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with concise summaries, tables, and inline shell commands when API calls are needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAXHUB_API_KEY and curl; keeps API key values out of user-facing output.] <br>

## Skill Version(s): <br>
3.6.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
