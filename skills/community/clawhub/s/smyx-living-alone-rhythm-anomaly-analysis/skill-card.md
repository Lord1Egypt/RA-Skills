## Description:

Analyzes nighttime camera footage for lights-off time and early-morning activity, compares the observations with a personal baseline, and reports significant sleep-rhythm changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Family members and remote-care staff use the skill to compare nighttime observations with a 7–14-day personal baseline and prepare sleep-rhythm reports and check-in reminders. Results are monitoring prompts, not medical diagnoses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote service, identity or credential data sent, account creation, and video-submission controls are unclear; the security scan is also partial.

Mitigation: Before installation, ask the maintainer to explain the service, data sent, account controls, and video-submission controls, and resolve the missing scan reference.

Risk: Nighttime bedroom or living-room footage contains highly private information.

Mitigation: Obtain the person's informed consent and clarify how footage is handled before submitting video.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-living-alone-rhythm-anomaly-analysis)
- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Text, Guidance]

**Output Format:** [Structured analysis reports in JSON; historical report lists in Markdown tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include lights-off time, early-morning activity, baseline comparisons, anomaly prompts, recommendations, and report links.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
