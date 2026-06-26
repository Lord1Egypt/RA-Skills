## Description: <br>
Create and edit Tally forms via API for building surveys, feedback forms, or questionnaires programmatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yujesyoga](https://clawhub.ai/user/yujesyoga) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use this skill to list, read, update, and back up Tally forms while generating survey, feedback, and questionnaire structures through the Tally API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to use a Tally API key to list, read, and update forms. <br>
Mitigation: Use a dedicated or least-privileged API key and confirm form IDs and JSON payloads before updates. <br>
Risk: Downloaded backups or submissions may contain sensitive respondent data. <br>
Mitigation: Treat backups and submissions as sensitive data and store, share, and delete them according to the user's data-handling requirements. <br>
Risk: Incorrect form block JSON could break or misconfigure a Tally form. <br>
Mitigation: Back up the form before patching it and verify the resulting block count and rendered form after the update. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yujesyoga/tally) <br>
- [Tally forms API endpoint](https://api.tally.so/forms) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Tally form block JSON, curl commands, backup steps, and verification guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
