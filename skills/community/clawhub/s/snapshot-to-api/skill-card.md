## Description: <br>
Discover hidden APIs behind web pages and replace expensive browser snapshots with lightweight API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ianzlm](https://clawhub.ai/user/ianzlm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to discover read-only page APIs, test their responses, and replace large browser snapshots with focused API calls when structured web data is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a logged-in browser session to inspect and call page APIs. <br>
Mitigation: Use it only on pages and data sources the user is authorized to access, and avoid banking, admin, account, or personal-data-heavy pages unless that access is explicitly intended. <br>
Risk: Discovered API URLs or notes may include tokens, tenant IDs, personal data, or session-specific parameters. <br>
Mitigation: Redact sensitive values before saving API notes or updating downstream skills. <br>
Risk: Removing or changing API parameters can silently return empty or incomplete data. <br>
Mitigation: Verify field counts and response completeness after parameter tuning, and keep browser snapshots as a fallback when APIs change or authentication expires. <br>


## Reference(s): <br>
- [Snapshot vs API: Detailed Comparison](references/comparison.md) <br>
- [ClawHub skill page](https://clawhub.ai/ianzlm/snapshot-to-api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Analysis, Code, API Calls] <br>
**Output Format:** [Markdown with JavaScript snippets and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include discovered endpoint paths, required query parameters, response-shape notes, and fallback guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
