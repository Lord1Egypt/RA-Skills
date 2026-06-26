## Description: <br>
Using a fixed camera in rehabilitation centers or homes, this skill analyzes children's behavior videos with pose estimation and temporal action detection to recognize repetitive stereotyped behaviors such as spinning, hand flapping, and body rocking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, therapists, caregivers, and developers use this skill to submit fixed-camera child behavior videos or URLs to a cloud analysis service and receive objective stereotyped-behavior event counts, durations, trends, and report links. The skill is intended to support review by qualified professionals and caregivers, not to diagnose autism or prescribe interventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill handles sensitive children's videos and identity-linked history through cloud workflows that are not clearly scoped. <br>
Mitigation: Use only with explicit guardian consent, confirmed retention and deletion rules, and a clear access-control model for reports and history. <br>
Risk: The security guidance flags bundled API key handling, account registration, and local token database behavior. <br>
Mitigation: Before deployment, verify that credentials are intentionally included, rotate or replace shared keys, and confirm that local token storage is encrypted and access-limited. <br>
Risk: The security guidance notes broad generic CRUD methods and unrelated health or pet artifacts in the bundle. <br>
Mitigation: Restrict runtime permissions and allowed endpoints to the behavior-analysis and report-query flows required for this release. <br>
Risk: The security verdict is suspicious. <br>
Mitigation: Install only after trusting the publisher and completing independent operational review for privacy, cloud data transfer, and report access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-autism-stereotyped-behavior-detect-analysis) <br>
- [API interface documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files] <br>
**Output Format:** [Markdown and JSON-formatted text, with optional saved result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include event-level behavior records, summary metrics, trend comparisons, report messages, history lists, and report export links.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
