## Description:

Find unique homestays and B&Bs with local character, host recommendations, authentic experiences, guest-rating sorting, and booking links powered by Fliggy through flyai CLI results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search for unique homestays, B&Bs, local stays, and related travel options using real-time flyai CLI output. It helps compare options in Markdown tables with booking links and a clear provenance tag for returned travel data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a globally installed, unpinned flyai npm CLI that handles travel searches and returns booking links.

Mitigation: Require explicit approval before installation, pin and verify the CLI version, and review the installed package before use.

Risk: The skill may persist raw travel queries and command history in .flyai-execution-log.json.

Mitigation: Disable or remove that logging behavior before use, especially when travel searches may contain personal or sensitive information.

Risk: Returned booking URLs are third-party links that may lead to payment or sign-in flows.

Mitigation: Validate booking URLs and destination domains before entering credentials or payment information.

## Reference(s):

- [Parameter and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Fallbacks](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/skills/unique-homestay)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be based on flyai CLI results, include a Powered by flyai tag, and avoid raw JSON.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
