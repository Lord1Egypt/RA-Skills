## Description:

Generate, edit, and manage PowerPoint presentations via the SlideSpeak API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mve](https://clawhub.ai/user/mve)

### License/Terms of Use:


## Use Case:

Developers and presentation authors use this skill to create PowerPoint presentations from text or uploaded documents, edit slides, list templates, download generated decks, and manage SlideSpeak task status through a Node.js helper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and uploaded documents are sent to the external SlideSpeak service.

Mitigation: Avoid confidential, regulated, or unapproved files and text unless external processing by SlideSpeak is permitted.

Risk: The skill requires a SlideSpeak API key.

Mitigation: Treat SLIDESPEAK_API_KEY like a password and avoid exposing it in prompts, logs, source control, or shared command output.

Risk: Presentation generation, editing, and document uploads can affect account usage, credits, or billing.

Mitigation: Confirm the target SlideSpeak account and expected credit impact before running generation or editing workflows.

Risk: Webhook configuration can send completion notifications to an external URL.

Mitigation: Use webhook URLs only when the destination is controlled and trusted.

## Reference(s):

- [SlideSpeak API Reference](artifact/references/API.md)
- [SlideSpeak homepage](https://slidespeak.co)
- [SlideSpeak developer settings](https://app.slidespeak.co/settings/developer)
- [ClawHub skill page](https://clawhub.ai/mve/skills/slidespeak)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Files]

**Output Format:** [Markdown guidance with Node.js commands and JSON command results; completed presentation downloads are PowerPoint files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SLIDESPEAK_API_KEY; most generation and editing operations are asynchronous and may return task IDs for polling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
