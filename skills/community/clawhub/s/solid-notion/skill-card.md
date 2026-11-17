## Description:

Read, edit, and write Notion pages as Markdown using the solid-notion CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentdchan](https://clawhub.ai/user/vincentdchan)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to manage Notion pages through the solid-notion CLI, including pulling pages as Markdown, editing content or properties, submitting changes with rollback behavior, restoring prior versions, and configuring Notion API authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on installing and trusting the third-party solid-notion npm package.

Mitigation: Install only from a trusted package source and review the package before using it with Notion data.

Risk: Notion API tokens and integration permissions can expose or modify shared pages.

Mitigation: Use stdin for token setup, avoid putting tokens in command lines or logs, and share only necessary Notion pages with the integration.

Risk: Write, submit, restore, or overwrite workflows can change Notion page content.

Mitigation: Review local diffs, command output, and history before publishing or restoring changes.

## Reference(s):

- [Notion integration setup](https://www.notion.so/profile/integrations/internal)
- [solid-notion Skill on ClawHub](https://clawhub.ai/vincentdchan/skills/solid-notion)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to run commands that read from or write to Notion and local solid-notion state.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
