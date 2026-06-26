## Description: <br>
从图片自动识别股票并加入股票池，使用 RapidOCR 提取股票代码，去重后按 FIFO 管理 30 只股票上限并保存到 manual_stock_list.json。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wy859](https://clawhub.ai/user/wy859) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading workflow operators use this skill to turn stock screenshots into a maintained local stock pool. It is intended to identify six-digit stock codes, avoid duplicates, and keep the list within a 30-stock limit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite and prune a local stock-list file used in trading workflows. <br>
Mitigation: Review the configured file path, back up manual_stock_list.json, and use dry-run or manual review before allowing saves or FIFO removals. <br>
Risk: OCR results may misread or miss stock codes from screenshots. <br>
Mitigation: Manually review recognized stock codes before relying on the updated stock pool in a trading process. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration] <br>
**Output Format:** [Terminal text plus JSON file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local stock-list JSON and may remove older entries when the configured 30-stock limit is exceeded.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
