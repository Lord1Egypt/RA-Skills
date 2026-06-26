## Description: <br>
PDCA+ISO9001质量管理 provides PDCA-cycle and ISO9001-based quality management support for lifecycle task control, standardized workflows, decision validation, continuous improvement, and quality reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yongjie666888](https://clawhub.ai/user/yongjie666888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, project leads, and quality-management teams use this skill to structure PDCA workflows, evaluate ISO9001-aligned controls, validate decisions, manage reusable knowledge, and generate quality reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved rules can be evaluated as Python expressions. <br>
Mitigation: Review or disable eval-based rule handling before installation, and use only trusted project and rule inputs. <br>
Risk: Knowledge-base data is persistent local storage. <br>
Mitigation: Avoid storing secrets or sensitive customer data, and apply local retention and cleanup controls. <br>
Risk: Report output paths are not safely constrained and HTML reports may include unsafe content. <br>
Mitigation: Restrict report filenames to safe basenames and sanitize HTML report content before sharing or publishing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yongjie666888/quality-management-pdca) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Self-Improving integration notes](artifact/docs/Self-Improving对接说明.md) <br>
- [Development integration notes](artifact/docs/开发方案对接说明.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, HTML, Configuration, Guidance] <br>
**Output Format:** [Markdown, JSON, HTML, and structured text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate project quality reports, ISO9001 validation reports, decision quality reports, statistics reports, check results, recommendations, and reusable knowledge entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
