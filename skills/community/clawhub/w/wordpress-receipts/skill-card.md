## Description:

Publish WordPress posts with API and public URL receipts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leostehlik](https://clawhub.ai/user/leostehlik)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to publish or verify WordPress posts and confirm that each publication has a matching API record and public URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security confidence is medium because analysis was partial and noted undeclared tool scope and persistence or purpose questions.

Mitigation: Before installing, consider whether the skill’s environment and network capabilities fit your needs, as the scan guidance recommends.

Risk: Publishing and verification use credentials with the configured WordPress API and make requests to the configured site.

Mitigation: Keep credentials in a private env file or pass them explicitly, and use the API and site you intend to authorize.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leostehlik/skills/wordpress-receipts)
- [Project homepage](https://github.com/LeoStehlik/wordpress-receipts)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON]

**Output Format:** [Markdown instructions with shell commands and JSON receipt examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Receipt examples report the post ID, status, canonical URL, and public HTTP status.]

## Skill Version(s):

0.1.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
