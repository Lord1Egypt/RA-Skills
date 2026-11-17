## Description:

Triage GitHub PRs and issues using vision-based scoring. Use when a user wants to prioritize, score, review, de-duplicate, or batch-process open pull requests or issues against their project's mission and values. Supports onboarding, scanning, and reporting for GitHub repositories via the gh CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patrob](https://clawhub.ai/user/patrob)

### License/Terms of Use:


## Use Case:

Developers and maintainers use this skill to onboard a repository, score open GitHub pull requests or issues against a project-specific vision, identify duplicates, and generate triage reports for review queues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository text can influence generated interview prompts and triage context.

Mitigation: Use trusted repositories or review the generated interview prompt before letting an agent act on it.

Risk: PR bodies, README content, release notes, and generated reports may contain untrusted or misleading text.

Mitigation: Treat these inputs and outputs as untrusted and require human review before labeling, closing, posting, or otherwise acting on triage recommendations.

Risk: Rule-based scores and duplicate indicators may be incomplete for ambiguous PRs.

Mitigation: Use the generated scores as prioritization guidance and manually review borderline or high-impact changes before making maintainer decisions.

## Reference(s):

- [Scoring Rubric Template](references/rubric-template.md)
- [Example Vision and PR Evaluation Framework](references/example-vision.md)
- [GitHub CLI](https://cli.github.com)
- [ClawHub skill page](https://clawhub.ai/patrob/skills/repo-pr-triage)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown]

**Output Format:** [Markdown guidance with shell commands, JSON score output, and generated Markdown triage reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an interview prompt, vision and rubric guidance, scored PR data, duplicate indicators, and prioritize/review/close/summary reports.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
