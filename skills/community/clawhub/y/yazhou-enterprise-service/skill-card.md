## Description: <br>
A Chinese-language enterprise-service skill for querying company information, recommending applicable policies, supporting safety-production supervision, and generating service reports for Yazhou District enterprises. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wing-art](https://clawhub.ai/user/wing-art) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Yazhou District enterprise-service, investment-promotion, and policy-consultation staff use this skill to gather company facts, match preferential policies, review safety-production posture, and produce single- or multi-company service reports. <br>

### Deployment Geography for Use: <br>
China, focused on Yazhou District, Sanya, Hainan <br>

## Known Risks and Mitigations: <br>
Risk: Company lookups and generated reports may include sensitive or confidential business information. <br>
Mitigation: Confirm that the lookup is necessary, avoid entering unnecessary confidential or personal data, and review generated .docx reports before sharing. <br>
Risk: Policy, financial, or safety-production conclusions may be outdated, incomplete, or tied to the wrong company identity. <br>
Mitigation: Verify the company identity and cross-check policy, financial, and safety conclusions against official sources before acting on the report. <br>
Risk: The skill depends on web search and companion skills, so output quality depends on those tools and their available sources. <br>
Mitigation: Use the skill only in workflows where web search and the documented dependent skills are available, and treat generated recommendations as review material rather than final determinations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wing-art/yazhou-enterprise-service) <br>
- [Policies Reference](references/policies.md) <br>
- [Safety Regulations Reference](references/safety-regulations.md) <br>
- [Enterprise Types Reference](references/enterprise-types.md) <br>
- [Industrial Development Reference](references/industrial-development.md) <br>
- [National Enterprise Credit Information Publicity System](http://www.gsxt.gov.cn/) <br>
- [Hainan Policy Service](https://hqzc.hainan.gov.cn/) <br>
- [Yazhou District Government](http://www.yazhou.gov.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Word documents (.docx) for service reports, with markdown/text drafts and shell command prompts when using the helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single-company and multi-company reports; may rely on web search, docx generation, and optional financial-data lookup.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
