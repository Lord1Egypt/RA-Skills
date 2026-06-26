## Description: <br>
Deploy projects to Vercel, Netlify, or Fly.io with framework auto-detection, deployment reporting, and rollback support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vanthienha199](https://clawhub.ai/user/vanthienha199) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to deploy web, Python, Node.js, static, or container projects to Vercel, Netlify, or Fly.io and inspect deployment status, logs, rollback options, and domains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Activation language is broad for workflows that can affect live deployments. <br>
Mitigation: Require explicit confirmation of the project, platform, and target environment before executing deployment commands. <br>
Risk: Deployment commands may use hosting credentials and affect production environments. <br>
Mitigation: Use the hosting CLI's built-in authentication, avoid storing or exposing API tokens, and default to preview or staging unless production is explicitly requested. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vanthienha199/quick-deploy) <br>
- [Publisher profile](https://clawhub.ai/user/vanthienha199) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and deployment reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose deployment, status, rollback, log, and domain-management commands; production deployment should require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
