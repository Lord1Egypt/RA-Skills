## Description: <br>
Audits live Shopify store and product pages for Google Merchant Center Misrepresentation policy risk by crawling public pages without a Shopify Admin API token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvsao](https://clawhub.ai/user/lvsao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External merchants, ecommerce operators, and agents supporting Shopify compliance use this skill to audit store and product pages before GMC submission, after suspension, or before an appeal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports forced automatic global update behavior before each use, which can change installed skill behavior without user approval. <br>
Mitigation: Review or remove the forced update step, pin an audited version, and require explicit approval before any global skill update. <br>
Risk: The audit is based on public crawling and cannot verify GMC account settings, feed contents, exact inventory, or some checkout and return-policy behavior. <br>
Mitigation: Treat uncertain findings as risk signals and complete the manual checklist before relying on the report for a GMC appeal or submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lvsao/shopify-gmc-misrepresentation-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/lvsao) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [HTML audit report with supporting Markdown guidance and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates a UTF-8 report with risk score, prioritized findings, evidence, manual checklist, and staged remediation plan.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
