## Description:

Fetches webpage content with a stealth-enabled headless browser and converts captured HTML into readable Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlutwuwei](https://clawhub.ai/user/dlutwuwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve webpages that need browser execution or basic anti-crawl handling, then inspect the page title and extracted Markdown content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Opening user-provided URLs in an unsandboxed browser without URL safeguards can expose internal resources if misused.

Mitigation: Run only in an isolated, non-privileged environment with no sensitive files, credentials, or internal network access, and use only URLs the operator is authorized to contact.

Risk: The skill does not validate public HTTP or HTTPS targets or block local and private addresses across redirects.

Mitigation: Prefer a revised version that validates public http/https URLs, blocks local and private address ranges across redirects, enables browser sandboxing, and pins dependencies with a lockfile.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dlutwuwei/skills/web-anti-crawl-fetch)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Console text with progress messages, page title, and Markdown content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Markdown output is truncated by the script after 20000 characters.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
