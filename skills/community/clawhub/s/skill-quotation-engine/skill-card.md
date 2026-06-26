## Description: <br>
智能报价引擎 — 根据设备清单和工时自动生成报价单 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zimuge-doudou](https://clawhub.ai/user/zimuge-doudou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Event production teams and developers use this skill to generate local quotation estimates from show equipment, labor, transport, insurance, management, and tax inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated quotation exports can overwrite an existing file if the same path is selected. <br>
Mitigation: Choose export paths deliberately and review the generated JSON before relying on it. <br>
Risk: The skill documentation references PDF export, but the available artifact evidence shows JSON export behavior. <br>
Mitigation: Verify the available export method before depending on PDF output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zimuge-doudou/skill-quotation-engine) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files] <br>
**Output Format:** [Plain text summaries, JSON quotation objects, and optional JSON export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local quotation calculator; generated JSON exports are written only to user-selected paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
