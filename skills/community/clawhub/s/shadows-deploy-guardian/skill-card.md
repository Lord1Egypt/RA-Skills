## Description: <br>
Pre-deployment verification checklist — tests, types, build, secrets scan, environment validation. Use before pushing to production or staging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NakedoShadow](https://clawhub.ai/user/NakedoShadow) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and release engineers use this skill before staging or production deployment to run a six-gate readiness check covering git state, tests, type and lint checks, builds, secret patterns, and environment validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The checklist runs repository test, lint, and build commands that may execute project code. <br>
Mitigation: Use it only in trusted repositories or inside a sandbox or CI environment before relying on the results. <br>
Risk: Secret-like matches from the grep-based scan can appear in terminal output. <br>
Mitigation: Run the scan in a private terminal session where output is not logged to shared systems. <br>
Risk: Git remote checks contact configured remotes and environment validation may contact DEPLOY_URL when set. <br>
Mitigation: Review configured remotes and target URLs before running the gates in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NakedoShadow/shadows-deploy-guardian) <br>
- [Publisher profile](https://clawhub.ai/user/NakedoShadow) <br>
- [Clawdis homepage](https://clawhub.ai/NakedoShadow) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with gate-status table and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces PASS, FAIL, SKIP, or warning statuses for deployment gates and does not auto-deploy.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact/SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
