## Description: <br>
Wxpush helps agents configure and send WeChat template-message pushes through edgeone, wxpush, or go-wxpush-compatible APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shisheng820](https://clawhub.ai/user/shisheng820) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Wxpush to configure WeChat push-message endpoints and generate curl or Python commands for sending template messages through edgeone, wxpush, or go-wxpush APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles real WeChat messaging credentials and may send them to the configured wxpush endpoint. <br>
Mitigation: Use a self-hosted or vetted endpoint, keep ~/.config/wxpush/wxpush.env private with 600 permissions, and rotate credentials that may have been exposed. <br>
Risk: URL-based token or AppSecret examples can expose secrets through terminal history, logs, or query strings. <br>
Mitigation: Prefer POST bodies or Authorization headers for secrets and avoid GET/query-string examples when sending real credentials. <br>


## Reference(s): <br>
- [EdgeOne API documentation](references/edgeone.md) <br>
- [Wxpush API documentation](references/wxpush.md) <br>
- [Go-WXPush API documentation](references/go-wxpush.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline curl and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that read ~/.config/wxpush/wxpush.env and call the configured wxpush endpoint.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
