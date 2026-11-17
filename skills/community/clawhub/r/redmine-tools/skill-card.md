## Description:

Fetch, update, and summarize Redmine issue attachments from CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinxianwei](https://clawhub.ai/user/yinxianwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support engineers use this skill to retrieve Redmine issue details, update issue status or notes, and summarize image attachments through a configured model endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Attachment download behavior can expose a Redmine API key to unintended endpoints.

Mitigation: Review before installing, use a dedicated least-privilege Redmine API key, and prefer a fixed version that validates full URL origins and prevents API-key forwarding across redirects.

Risk: The image command sends Redmine image attachments plus issue ID and subject context to a configured OpenAI-compatible endpoint.

Mitigation: Use the image command only with an endpoint approved for that data, and avoid running it on sensitive attachments unless that data transfer is acceptable.

## Reference(s):

- [ClawHub redmine-tools page](https://clawhub.ai/yinxianwei/skills/redmine-tools)
- [Skill definition](artifact/SKILL.md)
- [CLI source](artifact/scripts/redmine.js)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON]

**Output Format:** [Markdown with inline bash commands and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require Redmine credentials; image summaries require a configured OpenAI-compatible endpoint.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact frontmatter lists 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
