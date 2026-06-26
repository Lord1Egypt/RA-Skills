## Description: <br>
小红书关键词联想词批量采集工具 - 支持批量关键词导入、多轮次深度联想挖掘长尾词、自动去重、TXT/Excel双格式导出，适用于SEO优化、内容选题策划、种草关键词研究、竞品分析等场景。 <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[otzippo](https://clawhub.ai/user/otzippo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, SEO practitioners, and developers can use this skill to run a Python batch keyword expansion workflow for Xiaohongshu-style seed terms and generate deduplicated TXT or optional Excel reports. The current release should be treated as a workflow and report-format demonstration unless an authorized, documented data source is added. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Synthetic autocomplete suggestions may be mistaken for verified Xiaohongshu data. <br>
Mitigation: Treat reports as demonstration output unless the publisher implements and documents an authorized data source, and clearly label synthetic output in downstream use. <br>
Risk: Future API integration guidance could lead users to paste browser cookies, tokens, or session headers into local code. <br>
Mitigation: Do not paste credentials into the tool; use only documented, authorized access methods and store any required secrets outside the artifact. <br>
Risk: Automated platform querying can violate platform terms or create unreliable results if implemented without controls. <br>
Mitigation: Review Xiaohongshu terms, use conservative request delays, and validate results before using them for business decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/otzippo/xiaohongshu-keyword-batch-autocomplete) <br>
- [Publisher profile](https://clawhub.ai/user/otzippo) <br>
- [Xiaohongshu website](https://www.xiaohongshu.com) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands; generated TXT reports or optional Excel workbooks from the Python script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script accepts a single keyword or keyword file, depth 1-3, TXT or optional Excel output, output directory, delay, and deduplication settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
