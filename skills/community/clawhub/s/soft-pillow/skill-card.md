## Description: <br>
Use when the user asks about their sleep data, dream history, or wants to query sleep entries from the Soft Pillow app. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kivS](https://clawhub.ai/user/kivS) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External Soft Pillow users can let an agent read sleep status, list and inspect sleep entries, and search dreams or notes after they provide a Soft Pillow API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read sensitive sleep, dream, notes, disruption, mood, and activity-related history when an API key is available. <br>
Mitigation: Use a revocable Soft Pillow API key, share it only through secure local configuration, and limit queries to the entries needed for the task. <br>
Risk: Dream and sleep history could be exposed in chat transcripts, logs, or downstream summaries. <br>
Mitigation: Avoid pasting API keys into chat, do not request broad history unless needed, and redact or omit sensitive excerpts before sharing results. <br>
Risk: Continued API access may remain available after the immediate task is complete. <br>
Mitigation: Revoke the API key from Soft Pillow settings when agent access is no longer needed. <br>


## Reference(s): <br>
- [Soft Pillow homepage](https://paevita.com/en/soft-pillow) <br>
- [Soft Pillow on the App Store](https://apps.apple.com/us/app/soft-pillow/id6757248808) <br>
- [ClawHub skill page](https://clawhub.ai/kivS/soft-pillow) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with API examples and JSON response snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOFT_PILLOW_API_KEY; responses may include sensitive sleep and dream history.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
