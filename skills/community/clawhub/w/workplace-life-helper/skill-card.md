## Description: <br>
Openclaw Skill helps agents call paid workplace and life-assistance APIs for rental issues, resale listings, workplace writing, resumes, reports, and content compliance checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jie868](https://clawhub.ai/user/jie868) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to route workplace, rental, resale, and content-compliance requests to a paid remote API and present the returned guidance or generated text in a readable form. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted workplace, rental, contract, resume, dispute, or business text is processed by a remote paid service. <br>
Mitigation: Use the skill only when that processing is acceptable, and redact unnecessary personal, confidential, or sensitive details before sending requests. <br>
Risk: The skill can trigger paid API usage through the disclosed Alipay A2M payment flow. <br>
Mitigation: Confirm each paid use and the 0.10 CNY per-call price before authorizing payment. <br>
Risk: Legal, compliance, pricing, and workplace outputs may be incomplete or unsuitable as professional advice. <br>
Mitigation: Treat results as reference material and review important decisions with qualified professionals or relevant internal reviewers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jie868/workplace-life-helper) <br>
- [Publisher profile](https://clawhub.ai/user/jie868) <br>
- [Service API endpoint](https://w4h8ghmxcv.coze.site) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown-formatted text with JSON API responses and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calls a paid remote API and may return payment-required details before producing the requested result.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
