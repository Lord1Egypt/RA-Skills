## Description:

Provides a Tkinter localization pattern for Chinese and English with system-language detection, a persistent manual switch, and a translation fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add Chinese and English language selection, startup language detection, and persistent preferences to Tkinter desktop applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The supplied security analysis reports that the language-switching pattern may not translate the interface as promised.

Mitigation: Review translation coverage for all visible UI text and verify both languages in the target application.

Risk: Changing languages restarts the application and may leave unsaved work unprotected.

Mitigation: Save or otherwise protect user changes before restarting the application to apply a language choice.

Risk: The security analysis was partial, with unresolved referenced paths and a PNG outside its static-analysis scope.

Mitigation: Review the supplied source materials and validate the resulting code before installing or running it.

## Reference(s):

- [Tkinter i18n Template](references/i18n_template.py)
- [ClawHub Skill Page](https://clawhub.ai/oracis/skills/tkinter-i18n)

## Skill Output:

**Output Type(s):** [Code, Guidance, Configuration instructions]

**Output Format:** [Markdown guidance with Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a Tkinter localization pattern and translation table.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
