## Description: <br>
A WeChat cover-design skill that uses RedFox trend data to analyze high-performing article covers, produce a local HTML analysis report, and generate cover design proposals with image-generation prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyi-github](https://clawhub.ai/user/yuanyi-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
WeChat Official Account creators, content operators, media editors, and design teams use this skill to compare recent high-performing cover patterns, prepare a visual analysis report, and choose among cover design proposals before generating a 2.35:1 cover image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key and may expose unpublished article or reference details in debug output or generated reports. <br>
Mitigation: Keep REDFOX_API_KEY private, avoid sharing debug output or generated reports containing sensitive details, and review generated HTML before public distribution. <br>
Risk: Generated cover recommendations may depend on incomplete or time-limited trend data. <br>
Mitigation: Review the report and source examples before relying on the proposals for publication or campaign decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuanyi-github/wechat-cover-generator) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [WeChat explosive cover data format](references/gzh_trend_data_format.md) <br>
- [Cover analysis report template](references/report_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, HTML, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON-derived analysis, a generated local HTML report, image-generation prompts, and a final cover image after user selection.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a REDFOX_API_KEY environment variable and uses RedFox trend data limited to roughly yesterday through the previous 30 days.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
