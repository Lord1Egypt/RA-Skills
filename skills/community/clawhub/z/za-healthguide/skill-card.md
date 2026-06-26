## Description: <br>
Helps users with prior illnesses or abnormal health indicators compare health-insurance eligibility, underwriting rules, and product options for ZhongMinBao and other insurers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hellonorth](https://clawhub.ai/user/hellonorth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and insurance advisors use this skill to structure health-insurance questions, compare underwriting outcomes, and prepare compliant guidance for users with existing conditions or abnormal health indicators. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive health-insurance details may be sent to ZhongAn iHealth or search providers without clear user notice or consent. <br>
Mitigation: Use only non-identifying health details, obtain consent before external lookup, and redact personal identifiers from all queries. <br>
Risk: The artifact includes an embedded API key for the product knowledge service. <br>
Mitigation: Replace the embedded key with a managed credential, rotate the exposed key, and limit access to the minimum required scope. <br>
Risk: Insurance guidance may be mistaken for a final underwriting, medical, or claims decision. <br>
Mitigation: Keep disclaimers visible, cite official product terms, and direct users to the insurer or qualified professionals for final decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hellonorth/za-healthguide) <br>
- [Compliance Rules](references/compliance-rules.md) <br>
- [ZhongMinBao Product Reference](references/zhongminbao-products.md) <br>
- [Other Insurer Product Reference](references/other-products.md) <br>
- [ZhongAn iHealth Product Page](https://ihealth.zhongan.com/wxmp/pages/index) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with product comparisons, underwriting caveats, compliance disclaimers, and optional shell commands for product knowledge queries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rely on external ZhongAn iHealth and search-provider queries; users should avoid personal identifiers and confirm final terms with the insurer.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
