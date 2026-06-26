## Description: <br>
Deploy local web projects to live URLs by automating GitHub repo creation, Vercel/Netlify deployment, and optional custom domain setup with SSL and CI/CD. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h4gen](https://clawhub.ai/user/h4gen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to publish local web projects to production URLs, set up a GitHub-backed deployment path, and document custom-domain steps when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deployment actions can publish local code and change hosting or domain state. <br>
Mitigation: Confirm repository visibility, selected deploy target, production deployment, and domain changes before proceeding. <br>
Risk: Credentials or account context may grant broader access than intended. <br>
Mitigation: Use least-privilege GitHub, Vercel, Netlify, and Maton credentials, and verify the logged-in accounts before deployment. <br>
Risk: Local project secrets could be pushed or deployed accidentally. <br>
Mitigation: Scan the project for secrets before repository creation, push, or production deployment. <br>
Risk: Dependent skills or broad updates can change deployment behavior. <br>
Mitigation: Review dependent skills, install only the deploy path needed, and avoid update-all operations unless explicitly intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/h4gen/web-hosting) <br>
- [Inspected upstream skills](references/inspected-skills.md) <br>
- [ClawHub](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with structured status sections and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports project detection, repository status, infrastructure gates, deployment status, custom-domain plan, and next actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
