## Description: <br>
Audit Shopify tracking integrity across UTM, pixel, CAPI, and checkout events to detect attribution leaks. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[Leooooooow](https://clawhub.ai/user/Leooooooow) <br>

### License/Terms of Use: <br>
CC BY-NC-SA 4.0; server evidence lists MIT-0 <br>


## Use Case: <br>
Performance marketers, ecommerce operators, and analytics teams use this skill to inspect Shopify event evidence, pixel/CAPI configuration notes, UTM samples, and checkout flow maps for attribution gaps that can distort ROAS and conversion reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit inputs may include customer PII, secrets, API tokens, or unrelated Shopify store data. <br>
Mitigation: Provide only the tracking samples and configuration details needed for the audit, and redact customer PII, secrets, API tokens, and unrelated store data. <br>
Risk: The audit report could confuse tracking collection failures with real performance changes if evidence is incomplete. <br>
Mitigation: Tie findings to concrete event evidence, mark assumptions when full logs are unavailable, and validate recommended fixes before changing production tracking or campaign decisions. <br>
Risk: The artifact license text states non-commercial CC BY-NC-SA terms while server evidence lists MIT-0. <br>
Mitigation: Confirm the applicable license terms with the publisher before commercial reuse or redistribution. <br>


## Reference(s): <br>
- [Shopify Tracking Auditor release page](https://clawhub.ai/Leooooooow/shopify-tracking-auditor) <br>
- [Output template](artifact/references/output-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, analysis] <br>
**Output Format:** [Markdown report with an executive summary, prioritized actions, evidence table, and 7-day execution plan] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings should be tied to concrete event evidence, with assumptions marked when complete logs are unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
