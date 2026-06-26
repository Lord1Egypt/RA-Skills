## Description: <br>
Wayfound helps an agent add lightweight self-review by creating a SOUL.md rubric, setting up an optional daily OpenClaw review cron job, and writing concise review notes into memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cburnette](https://clawhub.ai/user/cburnette) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use Wayfound to add an ongoing self-review habit to an OpenClaw agent, using daily memory review and a small rubric to surface recurring quality, safety, or workflow issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates an ongoing local self-review habit that can retain sensitive details in long-lived memory files. <br>
Mitigation: Review generated memory files and SOUL.md updates periodically, and avoid storing credentials, personal data, or other sensitive details in review notes. <br>
Risk: The daily review cron job changes agent behavior over time and may create duplicate scheduled jobs if configured repeatedly. <br>
Mitigation: Require explicit user approval before setup, check the existing cron list first, confirm where review files are written, and document how to disable the job. <br>
Risk: Self-review can miss blind spots or rationalize mistakes because the agent evaluates its own behavior. <br>
Mitigation: Treat review notes as prompts for user-visible follow-up when issues recur or feel uncertain, rather than as independent assurance. <br>


## Reference(s): <br>
- [Wayfound homepage](https://wayfound.ai) <br>
- [ClawHub listing](https://clawhub.ai/cburnette/wayfound) <br>
- [Rubric Examples](references/rubric-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and review-file examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce short daily review notes in memory/review-YYYY-MM-DD.md when the user approves the cron setup.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
