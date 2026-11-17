## Description:

Smart note-taking skill that saves requested development notes to workspace memory and a SumoNoteBook shared folder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sumo0221](https://clawhub.ai/user/sumo0221)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other ClawHub users use this skill to capture development notes on request, saving Markdown records locally and syncing copies to a SumoNoteBook shared folder.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can copy development notes or conversation content into an outside shared notebook path without a separate confirmation step.

Mitigation: Use it only for content intended to be retained in both workspace memory and the SumoNoteBook raw/shared folder; avoid secrets, credentials, proprietary discussions, and private conversation text.

Risk: The script writes files to local workspace memory and a fixed SumoNoteBook shared directory.

Mitigation: Confirm the configured paths are appropriate for the environment before use and review saved Markdown files for unintended sensitive content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sumo0221/skills/sumo-smart-note)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands]

**Output Format:** [Markdown note files with terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes to workspace memory and SumoNoteBook raw/shared; workspace entries are deduplicated by content hash.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
