## Description:

Check an AI built app for 5 common quality problems before launch. Use when a user asks to review, audit, or check an app built with AI, or asks why an app feels slow, confusing, or crashy. Give it a folder of app files, a demo link, or a description of the app and it returns a pass/fail report with evidence and fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mmsample97](https://clawhub.ai/user/mmsample97)

### License/Terms of Use:

MIT

## Use Case:

External users and small business owners can use the skill to review an AI-built app before launch. It checks navigation, save feedback, list pagination, database call patterns, and background work, then reports evidence and prioritized fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewing consequential jobs, including bulk messaging, could affect real users or services if run against a live environment.

Mitigation: Use isolated staging with synthetic data, test recipients, mocked external services, and bounded workloads. Require explicit authorization for real messaging or other consequential operations; otherwise inspect code and report runtime behavior as untested.

## Reference(s):

- [Server-resolved source repository (commit 81a8764b5730b5f07a8b6b6333284d3aa1b3dca0)](https://github.com/mmsample97/vibe-app-quality-checker)
- [ClawHub skill page](https://clawhub.ai/mmsample97/skills/vibe-app-quality-checker)
- [Publisher profile](https://clawhub.ai/user/mmsample97)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with a five-check results table, evidence, prioritized fixes, owner steps, and quality notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-based findings; checks that cannot be verified from the supplied material are identified as needing code access or otherwise left unverified.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
