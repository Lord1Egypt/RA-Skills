## Description: <br>
Complete Ryot media tracker with progress tracking, reviews, collections, analytics, calendar, and automated daily/weekly reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[f-liva](https://clawhub.ai/user/f-liva) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to manage a Ryot media tracker from an agent, including media search, progress updates, reviews, collections, analytics, calendars, and report automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Ryot API token and can update tracker data, including bulk episode progress. <br>
Mitigation: Protect the Ryot config file and confirm media IDs, ratings, collection IDs, and episode ranges before running update commands. <br>
Risk: The optional automation setup can create recurring reports sent to a WhatsApp number. <br>
Mitigation: Run the automation setup only when recurring reports are desired, and verify the destination number and schedule before enabling it. <br>


## Reference(s): <br>
- [ClawHub Ryot release](https://clawhub.ai/f-liva/ryot) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Ryot instance URL and API token; some commands update tracker data or configure recurring reports.] <br>

## Skill Version(s): <br>
1.2.0 (source: evidence release, CHANGELOG, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
