## Description: <br>
Detect config drift between required local env keys and a Render service before deploy; fails when required keys are missing remotely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and release engineers use this skill before deployment to compare required local environment keys with the keys configured on a Render service and catch missing remote configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Render API key is required for live API checks and may grant access beyond this comparison task. <br>
Mitigation: Use a least-privilege Render API key where possible and provide it only through trusted local or CI secret handling. <br>
Risk: Environment key names and drift results may appear in terminal or CI logs. <br>
Mitigation: Review log visibility before sharing output, especially when key names reveal sensitive infrastructure details. <br>
Risk: Changing RENDER_API_BASE_URL can direct requests to a non-Render endpoint. <br>
Mitigation: Keep RENDER_API_BASE_URL at the default Render endpoint unless a trusted endpoint is intentionally being tested. <br>


## Reference(s): <br>
- [Render API base URL](https://api.render.com/v1) <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/render-deploy-diff) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Analysis, Guidance] <br>
**Output Format:** [Terminal text with service identity, key counts, drift lists, result status, and process exit code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns exit code 0 when all required keys exist on Render and exit code 1 when required keys are missing or inputs are invalid.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
