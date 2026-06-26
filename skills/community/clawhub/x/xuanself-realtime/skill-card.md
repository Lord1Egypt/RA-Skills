## Description: <br>
俄罗斯血糖检测设备市场调研（即时版）整合 Python 脚本化报告生成、SerpAPI 实时搜索、智能数据解析和 Xuanself 10 章节结构，生成可交付的俄罗斯血糖检测设备市场调研报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxuan1992asia-svg](https://clawhub.ai/user/wangxuan1992asia-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business, market intelligence, and medical-device teams use this skill to generate Russian blood glucose monitoring device market reports from packaged or user-provided data. It produces structured Markdown and Word report files covering market size, competitors, prices, policy, patient data, procurement, and entry recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes plaintext API credential handling and an apparent TGStat key in its data source configuration. <br>
Mitigation: Treat packaged keys as exposed, remove them before use, and store SerpAPI or TGStat credentials in environment variables or an untracked local configuration file. <br>
Risk: The generated report can contain current medical-market, social-media, price, policy, or procurement claims that may be incomplete or stale. <br>
Mitigation: Verify report claims against authoritative sources before using the output for commercial decisions or external distribution. <br>
Risk: The skill executes Python scripts and writes report outputs from local input data. <br>
Mitigation: Run it from the skill directory in a virtual environment and keep generated outputs in a dedicated folder. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangxuan1992asia-svg/xuanself-realtime) <br>
- [SerpAPI](https://serpapi.com) <br>
- [Packaged README](artifact/README.md) <br>
- [Packaged skill definition](artifact/SKILL.md) <br>
- [Packaged data source configuration](artifact/data/data_sources.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown report and generated .docx file, with setup guidance and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python dependencies and user-managed API credentials; generated reports should be fact-checked before business use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; packaged skill metadata states 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
