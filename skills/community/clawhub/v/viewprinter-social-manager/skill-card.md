## Description:

Helps manage connected ViewPrinter social accounts by preparing and publishing posts, managing media and account groups, and reviewing performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1vmgm](https://clawhub.ai/user/1vmgm)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams with a connected ViewPrinter account use this skill to schedule or publish social posts, manage media and account groups, and review account and post performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing may immediately expose content on real public accounts and cannot be recalled by this skill.

Mitigation: Confirm the content, destinations, labels, and resolved posting time with the user before publishing; report actual outcomes after the request completes.

Risk: Deleting media permanently removes stored files, and changing group membership can affect future posting destinations.

Mitigation: Review the selected media or group and the requested change with the user before proceeding.

Risk: Listing posts or media can disclose information across the user's ViewPrinter workspaces.

Mitigation: Only access connected accounts for the user's requested task and avoid sharing unrelated workspace information.

## Reference(s):

- [ViewPrinter Social Manager release](https://clawhub.ai/1vmgm/skills/viewprinter-social-manager)
- [Publisher profile](https://clawhub.ai/user/1vmgm)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports posting outcomes and performance by destination when available.]

## Skill Version(s):

1.3.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
