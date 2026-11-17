## Description:

Automatically filters livestream creators in Buyin/Jinritemai Creator Square using user-specified criteria and saves matching results to an Excel file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uncrowned-king](https://clawhub.ai/user/uncrowned-king)

### License/Terms of Use:

MIT-0

## Use Case:

External commerce operators and agent users use this skill to search for livestream creators by category, audience, follower count, creator level, and gender, then export matching creator records for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates a logged-in Buyin/Jinritemai business account.

Mitigation: Use a dedicated account or browser profile when possible and verify the selected account before relying on exported results.

Risk: Browser sessions are reused and API traffic is intercepted during the task.

Mitigation: Run the skill only in an account context where that automation is acceptable, and avoid sharing the browser profile with unrelated work.

Risk: The skill can save sensitive debug files without enough user control.

Mitigation: Review and delete any Desktop debug files after each run.

Risk: Generated Excel files may contain creator-controlled fields that are not formula-sanitized.

Mitigation: Treat generated Excel files as untrusted and inspect or sanitize them before opening in spreadsheet software.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uncrowned-king/skills/salesman-recommender)
- [Buyin/Jinritemai Creator Square](https://buyin.jinritemai.com/dashboard/servicehall/daren-square)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, files]

**Output Format:** [Text guidance with Python filter dictionaries and Excel (.xlsx) file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes matched creator records to an Excel file and may prompt for account login details when no active session is available.]

## Skill Version(s):

2.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
