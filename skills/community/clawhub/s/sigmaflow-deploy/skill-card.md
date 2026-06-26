## Description: <br>
Deploy the SigmaFlow SvelteKit trading frontend to the Git repository by cloning or updating the repo, installing dependencies, building the app, and pushing changes to the GitLab instance at git.homelab:3000. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sirenday](https://clawhub.ai/user/sirenday) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build and deploy the SigmaFlow SvelteKit frontend after feature work, bug fixes, or other code changes. It automates repository setup, dependency installation, production build, commit creation, and branch push. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The deployment helper embeds a reusable Git token. <br>
Mitigation: Rotate the exposed token, remove credentials from the skill, and use user-provided secrets through HTTPS, SSH, or a secret manager. <br>
Risk: The deployment flow can stage, commit, and push local changes automatically. <br>
Mitigation: Inspect the diff before staging and push through reviewed branches with branch protections instead of pushing directly to main. <br>
Risk: The script targets a specific SigmaFlow repository and GitLab instance. <br>
Mitigation: Run it only when you control that repository and have confirmed the target remote and branch. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sirenday/sigmaflow-deploy) <br>
- [SigmaFlow Svelte Repository](http://git.homelab:3000/vitali/SigmaFlow-Svelte) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Terminal status text with shell command effects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create commits and push changes to the configured Git branch.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
