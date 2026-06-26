## Description: <br>
Deploy static HTML/CSS/JS websites, landing pages, and single-page apps to W-Spaces with project creation, code push, and deployment via API key authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trandactruong](https://clawhub.ai/user/trandactruong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create and manage W-Spaces projects, push static HTML/CSS/JS content, and deploy public sites to wspaces.app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: W-Spaces API keys can grant deployment and key-management access. <br>
Mitigation: Use a dedicated API key, avoid pasting real credentials into chat or committing them to files, and revoke keys that are no longer needed. <br>
Risk: A custom WSPACES_API_URL could send credentials or deployment content to an unintended endpoint. <br>
Mitigation: Leave WSPACES_API_URL unset unless the endpoint is known and trusted. <br>
Risk: Deploy actions can publish static site content to a public wspaces.app URL. <br>
Mitigation: Review site contents before pushing or deploying and confirm deployment actions before they run. <br>
Risk: API key creation or revocation changes account access. <br>
Mitigation: Confirm any key creation or revocation action before executing the relevant script. <br>


## Reference(s): <br>
- [W-Spaces Public API v1](references/wspaces-api.md) <br>
- [W-Spaces](https://wspaces.app) <br>
- [W-Spaces API](https://api.wspaces.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WSPACES_API_KEY, curl, and jq; actions may publish static site content to W-Spaces.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
