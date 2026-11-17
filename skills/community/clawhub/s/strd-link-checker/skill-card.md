## Description:

Checks links in website HTML files and reports broken, redirected, slow, internal, external, and affiliate links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kryzl19](https://clawhub.ai/user/kryzl19)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site operators, and content teams use this skill to audit website HTML after publishing or during recurring site health checks, with additional reporting for affiliate links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound HEAD requests to every discovered link from the user's machine or CI environment.

Mitigation: Run it only on trusted site content, preferably inside a network-isolated runner, and review destinations before execution when possible.

Risk: The release evidence notes missing destination validation, private-address blocking, redirect controls, and dry-run or allowlist support.

Mitigation: Add or enforce an allowlist, block private network ranges, constrain redirects, and provide a dry-run mode before using it in sensitive environments.

## Reference(s):

- [Link Checker ClawHub skill page](https://clawhub.ai/kryzl19/skills/strd-link-checker)
- [kryzl19 publisher profile](https://clawhub.ai/user/kryzl19)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with shell command usage and environment variable configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include summary counts and link-level status details for broken, redirected, slow, and affiliate links.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
