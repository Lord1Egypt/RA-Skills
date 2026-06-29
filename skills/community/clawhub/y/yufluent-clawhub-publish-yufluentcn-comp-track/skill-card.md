## Description: <br>
Analyzes manually supplied competitor listing text across titles, bullets, descriptions, and keywords, then returns differentiation suggestions through the Yufluent cloud harness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metahuan](https://clawhub.ai/user/metahuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce operators and agents use this skill to compare their product listing against manually pasted competitor listing copy for Amazon, Shopify, or TikTok and identify practical differentiation opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pasted competitor text, optional listing text, and the Yufluent API key are sent to the configured Yufluent endpoint. <br>
Mitigation: Use the skill only when Yufluent processing terms are acceptable, avoid confidential launch plans, personal data, or trade secrets, and do not set TOKENAPI_BASE_URL to an untrusted host. <br>
Risk: The output is comparative guidance and may be incorrect or misleading for ranking, traffic, or market claims. <br>
Mitigation: Review results before use and treat them as advisory rather than a promise of platform ranking or traffic outcomes. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/metahuan/yufluent-clawhub-publish-yufluentcn-comp-track) <br>
- [Yufluent homepage](https://claw.changzhiai.com) <br>
- [Yufluent OpenClaw setup](https://claw.changzhiai.com/app/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Formatted text or JSON returned by the Yufluent skill run, with optional shell commands and configuration steps for invocation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOKENAPI_KEY and may use TOKENAPI_BASE_URL to select the Yufluent endpoint.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
