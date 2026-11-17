## Description:

Processes commented screenshots by saving them to a notes library, extracting key content, categorizing the item, setting a one-week reminder, logging observed patterns, and confirming what was saved.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enzoricciulli](https://clawhub.ai/user/enzoricciulli)

### License/Terms of Use:


## Use Case:

External users or personal knowledge-management agents use this skill to turn shared screenshots and accompanying comments into organized notes, reminders, and pattern logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically preserve shared screenshots and commentary in local notes without clear pre-action confirmation.

Mitigation: Narrow the trigger, require confirmation before writes, and avoid using the skill with sensitive screenshots.

Risk: Descriptive filenames and note destinations derived from screenshot context can create unsafe or messy paths if not handled carefully.

Mitigation: Sanitize filenames and use structured file operations constrained to approved notes directories.

Risk: Automatic one-week reminders can create unwanted follow-up tasks when the screenshot is misclassified.

Mitigation: Confirm the reminder topic and date, and honor user-provided reminder overrides.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/enzoricciulli/skills/screenshot-capture)
- [Publisher profile](https://clawhub.ai/user/enzoricciulli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown note entries, shell command snippets, reminder text, and brief text confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local note files and reminders when the hosting agent has those capabilities.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
