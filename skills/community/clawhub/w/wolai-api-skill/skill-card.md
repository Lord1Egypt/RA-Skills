## Description:

Operates Wolai notes, pages, blocks, and databases through Wolai's REST API using PowerShell-oriented workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cizixiu](https://clawhub.ai/user/cizixiu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to read, create, and update Wolai page content and database rows from an agent using Wolai API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A permanent Wolai app token could expose pages and databases granted to the app if pasted into chat, logs, or transcripts.

Mitigation: Store WOLAI_TOKEN in a secure credential or environment mechanism, avoid printing it, and rotate it immediately if exposure is suspected.

Risk: The skill can act on Wolai content within the app's granted permissions.

Mitigation: Grant the Wolai app only the minimum page and database permissions required for the intended workflow.

## Reference(s):

- [Wolai API base URL](https://openapi.wolai.com/v1)
- [Wolai developer center](https://www.wolai.com/dev)
- [ClawHub skill page](https://clawhub.ai/cizixiu/skills/wolai-api-skill)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with PowerShell code blocks and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Wolai app token supplied through WOLAI_TOKEN and access only to Wolai pages and databases granted to that app.]

## Skill Version(s):

1.0.7 (source: ClawHub release evidence; artifact frontmatter reports 1.0.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
