## Description:

Learns a user’s preferences through a local quiz and later feedback, then applies them to design, writing, naming, code, and product decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cutd](https://clawhub.ai/user/cutd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use xtaste to capture preferences and guide AI-assisted design, writing, naming, coding, and product decisions. It applies saved preferences to relevant tasks and records later user feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved preference excerpts may contain personal information and are retained in local plaintext logs; forgetting a signal does not remove its original log line.

Mitigation: Use `xtaste pause` to stop recording, and delete `~/.xtaste` (or the configured `XTASTE_HOME`) to erase stored data.

Risk: The first-use quiz may open automatically when no quiz is on file.

Mitigation: Close the quiz page, or install with `xtaste install --apply --no-onboard` to disable automatic quiz prompts.

## Reference(s):

- [ClawHub release](https://clawhub.ai/cutd/skills/xtaste)
- [Taste modeling method](references/method.md)
- [Preference dimensions](references/dimensions.json)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain-text preference context and task guidance; optional local browser quiz]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Personalized by domain and task scope; saved profile content is data, not instructions.]

## Skill Version(s):

0.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
