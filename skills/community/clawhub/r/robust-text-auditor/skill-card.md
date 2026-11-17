## Description:

Audits Chinese short-form video and livestream text by combining local rule scanning, Baidu content-review API results, and an LLM prompt for compliance reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahsbnb](https://clawhub.ai/user/ahsbnb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operations teams use this skill to review text for potential platform-compliance issues before publication. It produces a prompt that an agent can submit to an LLM to generate a risk report and revised text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audited content may be sent to Baidu and then to an LLM.

Mitigation: Use the skill only for content that is approved for remote processing, and obtain explicit user consent before sending sensitive text or files.

Risk: The skill stores Baidu credentials in the OpenClaw configuration.

Mitigation: Use scoped credentials, protect the configuration file, and rotate keys if the environment is shared or compromised.

Risk: The generated report is best-effort advice and may overstate certainty.

Mitigation: Treat results as review support, not a guarantee, and require human review before publishing or enforcing decisions.

Risk: An undocumented image command can upload local image files to Baidu.

Mitigation: Avoid using image review with sensitive files unless image upload is explicitly required and approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ahsbnb/skills/robust-text-auditor)
- [WeChat Channels content guide](https://weixin.qq.com/cgi-bin/readtemplate?lang=zh_CN&t=weixin_agreement&s=video_guide)
- [Baidu text censor API endpoint](https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined)
- [Baidu image censor API endpoint](https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/v2/user_defined)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Text prompt for LLM-based compliance report generation, with JSON snippets from local and remote review steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Baidu Cloud API credentials in the OpenClaw configuration and may create a final_prompt.txt file during use.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
