## Description:

Helps users authenticate to Meituan, claim available Meituan coupon benefits, and query coupon redemption history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meituan-openplatform](https://clawhub.ai/user/meituan-openplatform)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to complete Meituan SMS authentication, issue available coupon benefits, and retrieve prior coupon redemption records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Meituan phone/SMS login flow and stores account tokens locally.

Mitigation: Install only in trusted environments, isolate token storage where possible, and remove stored tokens when the account is no longer needed.

Risk: Command output and logs may expose full account tokens.

Mitigation: Treat logs and command output as sensitive, avoid sharing them, and prefer a release that redacts tokens before display or logging.

Risk: The skill passes sensitive values through command-line arguments and token verification flows.

Mitigation: Prefer an updated version that avoids command-line secrets and token-in-URL verification, and review process listings or shell history handling before use.

Risk: The artifact includes high-priority instruction language that attempts to limit caller control.

Mitigation: Review the skill before deployment and ensure the host agent enforces its own trusted instruction hierarchy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/meituan-openplatform/skills/waimai-coupon)
- [Meituan coupon skill page referenced by artifact](https://clawhub.ai/meituan-zhengchang/meituan-coupon)
- [Sankuai API documentation referenced by artifact](https://km.sankuai.com/collabpage/2752893495)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-facing user responses with JSON helper-script outputs and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes coupon issue status, coupon details, redemption history, authentication status, and error guidance.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
