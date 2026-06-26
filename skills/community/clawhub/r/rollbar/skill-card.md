## Description: <br>
Monitor and manage Rollbar error tracking by listing recent items, inspecting details, triaging issues, tracking deployments, and managing project access tokens through the Rollbar API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vittor1o](https://clawhub.ai/user/vittor1o) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Rollbar projects, review active errors, summarize top issues, and perform controlled triage actions from an agent workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles high-impact Rollbar access tokens, including account-level tokens that can manage projects and project tokens. <br>
Mitigation: Use least-privilege project tokens for routine monitoring and reserve account-level write tokens only for operations that require them. <br>
Risk: Workspace .env content is sourced as shell code during token resolution. <br>
Mitigation: Install and run the skill only in trusted workspaces where .env files are controlled and reviewed. <br>
Risk: The skill can persist newly created project tokens to .rollbar-mcp.json when --save is used. <br>
Mitigation: Avoid --save unless the resulting config file is protected and excluded from version control. <br>
Risk: Resolve, mute, activate, and project token management commands can change Rollbar state. <br>
Mitigation: Use --dry-run before mutating Rollbar state and require --yes only after reviewing the intended action. <br>


## Reference(s): <br>
- [ClawHub Rollbar skill page](https://clawhub.ai/vittor1o/rollbar) <br>
- [Rollbar API endpoint](https://api.rollbar.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON-formatted Rollbar API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Rollbar credentials and curl/python3; state-changing actions require --yes or --dry-run.] <br>

## Skill Version(s): <br>
1.5.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
