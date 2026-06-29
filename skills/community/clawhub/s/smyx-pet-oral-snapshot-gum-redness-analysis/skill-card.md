## Description: <br>
Analyzes pet oral snapshot images or videos from file uploads or URLs to classify gum color and tartar coverage, returning standardized oral-health observations for early care awareness without diagnosing disease. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and integrators of pet cameras, smart pet products, and pet health platforms use this skill to send oral snapshot media for cloud analysis and return structured observations about visible gum redness, tartar coverage, oral-health risk prompts, and report links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet media and report queries are sent to LifeEmergence/SMYX cloud services. <br>
Mitigation: Use the skill only where cloud processing is acceptable, disclose that media and report data leave the local environment, and review the service data-handling terms before deployment. <br>
Risk: The skill can silently create or reuse an account identity and persist tokens in the workspace. <br>
Mitigation: Run it in a controlled workspace, inspect stored token files during deployment review, and clear workspace state between users or tenants. <br>
Risk: Hidden open-id handling can affect historical report access if the host does not bind identity securely. <br>
Mitigation: Avoid direct use of hidden open-id parameters unless the host environment enforces authenticated identity binding and report access controls. <br>


## Reference(s): <br>
- [Pet Oral Snapshot API Documentation](artifact/references/api_doc.md) <br>
- [Shared Analysis API Documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-pet-oral-snapshot-gum-redness-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown and JSON structured analysis reports with optional saved output files and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call cloud APIs for analysis and historical report queries; results are oral-care observations, not medical diagnoses.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
