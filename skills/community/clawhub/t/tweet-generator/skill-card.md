## Description:

Craft tweets, threads, and viral hooks with schedule tips. Use when drafting copy, editing threads, optimizing engagement, scheduling posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

External social media writers and content teams use this skill to draft and refine short-form content, log content history, plan scheduled posts, search prior entries, and export local content records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Entered content is retained in local logs under ~/.local/share/tweet-generator.

Mitigation: Avoid sensitive, confidential, or embargoed text and clear local history according to local retention requirements.

Risk: CSV exports can expose user-entered content to spreadsheet handling risks.

Mitigation: Inspect or sanitize exported CSV values before opening them in spreadsheet software.

Risk: The script logs inputs but does not itself generate, optimize, or translate content.

Mitigation: Use the agent or a human reviewer for content generation and treat the script as local history and export tooling.

## Reference(s):

- [Tweet Generator on ClawHub](https://clawhub.ai/xueyetianya/skills/tweet-generator)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Plain text with shell command examples and optional JSON, CSV, or TXT exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores command history locally under ~/.local/share/tweet-generator.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter and script report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
