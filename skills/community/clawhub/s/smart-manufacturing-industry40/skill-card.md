## Description: <br>
面向制造业的AI智能体技能，支持生产排程优化、质量缺陷检测（视觉AI）、设备预测性维护、BOM物料管理、工业安全合规、MES/ERP数据对接。适用于离散制造和流程制造两大领域。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Manufacturing engineers, operations teams, and plant managers use this skill to analyze production schedules, product images, equipment telemetry, BOM data, and safety requirements for discrete and process manufacturing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Manufacturing datasets may contain trade secrets, customer-identifying records, plant-security details, regulated operational records, or full ERP/MES exports. <br>
Mitigation: Use only authorized, minimized, and redacted operational data for analysis. <br>
Risk: Predictive maintenance results depend on sufficient historical equipment data and may be unreliable with sparse or poor-quality telemetry. <br>
Mitigation: Validate maintenance recommendations against equipment history, maintenance records, and qualified engineering review before acting. <br>
Risk: Vision-based defect detection can be affected by lighting, image capture conditions, and inconsistent inspection setup. <br>
Mitigation: Standardize image acquisition conditions and confirm defect findings through the site quality process. <br>
Risk: Production scheduling recommendations may not capture all real-time shop-floor constraints. <br>
Mitigation: Review proposed schedules with operations staff and adjust them for current capacity, material availability, and safety constraints. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, structured data, guidance] <br>
**Output Format:** [Markdown or structured report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Gantt chart data, utilization estimates, defect distributions, CPK values, maintenance windows, spare-parts lists, MRP time series, purchasing suggestions, and safety-stock warnings.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
