## Description: <br>
Crawls Yindeng non-performing loan transfer announcements and results, optionally extracting structured financial data from downloaded PDFs with OCR and LLM analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiyouBug](https://clawhub.ai/user/aiyouBug) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and financial-data analysts use this skill to collect Yindeng announcement and result PDFs for a date range and generate Excel summaries. When analysis is enabled, extracted PDF text is sent to the configured LLM provider to produce structured financial fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Enabling analysis sends extracted PDF text to the configured LLM provider. <br>
Mitigation: Leave analysis disabled unless the user is allowed to share the downloaded announcement text with that provider, and review LLM_PROVIDER, LLM_API_BASE, and the provider privacy and retention terms before processing sensitive financial or legal details. <br>
Risk: The crawler downloads external PDFs and writes local PDF and Excel outputs. <br>
Mitigation: Install and run the skill in an isolated Python environment, then review generated files before relying on the extracted data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiyouBug/yindenganalyse) <br>
- [Yindeng transfer announcements source](https://www.yindeng.com.cn/xxpl/xxpl_bldkzr/bldkzr_zrgg/index.html) <br>
- [Yindeng transfer result announcements source](https://www.yindeng.com.cn/xxpl/xxpl_bldkzr/bldkzr_zrjggg/index.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, configuration] <br>
**Output Format:** [Plain text execution summary plus downloaded PDFs and Excel workbooks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional LLM analysis writes analysis_result.xlsx when credentials and provider configuration are supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
