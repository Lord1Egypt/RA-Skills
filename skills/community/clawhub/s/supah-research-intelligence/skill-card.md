## Description: <br>
Professional-grade web research with multi-source verification and credibility scoring. Cross-references multiple sources, scores reliability, and delivers verified intelligence for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[supah-based](https://clawhub.ai/user/supah-based) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to research topics, verify claims, score source credibility, and generate research reports with citations through SUPAH's web research API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad research prompts can send user content to a third-party paid service and may incur automatic micropayments with unclear consent or pricing boundaries. <br>
Mitigation: Use only with an x402 client that enforces per-call and total spending limits, confirm pricing with the publisher, and avoid submitting confidential claims, internal URLs, secrets, personal data, or proprietary research topics unless that disclosure is acceptable. <br>
Risk: The SUPAH_API_BASE environment variable can direct requests to a different service endpoint. <br>
Mitigation: Keep SUPAH_API_BASE set to a trusted HTTPS endpoint and review endpoint configuration before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/supah-based/supah-research-intelligence) <br>
- [SUPAH website](https://supah.ai) <br>
- [SUPAH API endpoint](https://api.supah.ai) <br>
- [x402 protocol](https://www.x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [CLI text output and Markdown-style research reports with source URLs and credibility or confidence scores] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a third-party HTTPS API and may incur x402 USDC micropayments up to the configured per-call maximum.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
