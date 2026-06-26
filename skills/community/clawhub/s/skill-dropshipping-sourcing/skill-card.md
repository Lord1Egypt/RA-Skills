## Description: <br>
Query CJ Dropshipping API v2.0 to source products and fetch details for catalog building. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to refresh CJ API access tokens, search CJ Dropshipping products by keyword, and produce normalized product JSON for catalog automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CJ API credentials are stored in a local cj-api.json file. <br>
Mitigation: Keep cj-api.json private, exclude it from source control, and restrict access to the local workspace where the skill runs. <br>
Risk: A changed baseUrl could send token or product requests to an unintended endpoint. <br>
Mitigation: Verify baseUrl points to the intended CJ API endpoint before refreshing tokens or sourcing products. <br>
Risk: Caller-selected output paths could overwrite unintended files. <br>
Mitigation: Use simple project-local output paths such as cj-results.json when running the sourcing script. <br>
Risk: The scripts depend on axios at runtime. <br>
Mitigation: Install axios from a trusted package source and review dependency provenance as part of deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zero2Ai-hub/skill-dropshipping-sourcing) <br>
- [CJ Dropshipping API v2.0 endpoint](https://developers.cjdropshipping.com/api2.0/v1) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local cj-api.json file for CJ API credentials and writes normalized search results to a caller-selected JSON output path.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
