## Description: <br>
Capture and manage TIL (Today I Learned) entries on OpenTIL using CLI commands for capture, extraction, publishing, editing, search, sync, and account management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biao29](https://clawhub.ai/user/biao29) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and knowledge workers use this skill to turn useful technical insights from a conversation or explicit command into OpenTIL entries, then manage drafts, publishing, sync, tags, categories, and account profiles without leaving the CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An OpenTIL token may allow reading, writing, publishing, and deleting entries. <br>
Mitigation: Use only the scopes needed for the intended workflow, protect ~/.til/credentials, and rotate the token if it may have been exposed. <br>
Risk: Conversation content may include secrets, customer data, proprietary details, or incident information that should not be captured or published. <br>
Mitigation: Review generated entries before syncing or publishing, and decline proactive capture suggestions in sensitive conversations. <br>
Risk: Management commands can publish, edit, unpublish, or delete OpenTIL entries. <br>
Mitigation: Require the documented confirmations for publish, edit, unpublish, and delete flows, especially the double confirmation before deletion. <br>


## Reference(s): <br>
- [OpenTIL Skill Page](https://clawhub.ai/biao29/til) <br>
- [OpenTIL](https://opentil.ai) <br>
- [API Reference](references/api.md) <br>
- [Management Subcommands Reference](references/management.md) <br>
- [Local Drafts and Sync Protocol](references/local-drafts.md) <br>
- [Auto-Detection Reference](references/auto-detection.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown entries, CLI status text, local draft files, and OpenTIL API requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can store drafts under ~/.til/drafts/ and credentials under ~/.til/credentials when configured by the user.] <br>

## Skill Version(s): <br>
1.11.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
