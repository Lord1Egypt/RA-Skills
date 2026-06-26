## Description: <br>
舟谱系统订单导入模板生成（自提订单+调拨订单分开，每表只有1个sheet）。当下单表数据需要转化为舟谱系统可导入的Excel格式时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xyzhangjf](https://clawhub.ai/user/xyzhangjf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations staff and agent users use this skill to convert order spreadsheets and price sheets into Zhoupu-compatible Excel import templates for pickup orders and transfer orders. The workflow includes a human approval step before generated files are uploaded to Zhoupu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes order and price spreadsheets that may contain sensitive business data. <br>
Mitigation: Run it only on the specific spreadsheets intended for conversion, keep processing local, and review generated Excel files before uploading them to Zhoupu. <br>
Risk: Incorrect quantities, barcode matches, prices, or document numbers could create bad import records. <br>
Mitigation: Keep the documented human approval step and compare generated totals, barcode warnings, and skipped items against the source spreadsheets before import. <br>
Risk: The scripts depend on spreadsheet-processing libraries and expected worksheet formats. <br>
Mitigation: Install required dependencies such as pandas and openpyxl, and rerun or manually correct records when the scripts report missing sheets, missing prices, or unmatched barcode data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xyzhangjf/zhoupu-order-import) <br>
- [Zhoupu portal](https://portal.zhoupudata.com/saas/main) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown instructions and generated Excel files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Zhoupu pickup-order and transfer-order import workbooks from user-provided order and price spreadsheets.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
