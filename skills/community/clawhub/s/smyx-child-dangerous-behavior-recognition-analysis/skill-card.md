## Description: <br>
Detects climbing, playing with fire, touching power sources, and dangerous actions near windows, providing real-time alerts for child safety supervision in homes, kindergartens, and nurseries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Caregivers, safety operators, and developers use this skill to analyze child-monitoring video or video URLs for hazardous behavior alerts, behavior counts, and structured report history. It supports supervision workflows but requires human confirmation of any safety-critical alert. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive child video, identifiers, account data, and report history with unclear service boundaries. <br>
Mitigation: Use it only with videos and identifiers that are authorized for LifeEmergence/SMYX remote services, avoid phone numbers or real names as open-id values, and treat history or export links as sensitive. <br>
Risk: Bundled or locally stored API credentials may expose access to remote services. <br>
Mitigation: Rotate or remove bundled API keys, avoid local token storage, and confirm authentication configuration before installation. <br>
Risk: Backend documentation is mismatched with the child-safety use case, which can obscure data handling, consent, and retention expectations. <br>
Mitigation: Require a purpose-specific child-safety API contract, explicit consent and retention terms, and updated documentation before production deployment. <br>


## Reference(s): <br>
- [Skill API documentation](references/api_doc.md) <br>
- [Analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-child-dangerous-behavior-recognition-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON reports with command-line examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local or remote alert summaries, dangerous-behavior counts, report history tables, and report links.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
