## Description:

Batch submit websites to AI tool directories and SEO directories to earn backlinks, with Playwright automation that checks free submissions and fills forms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kennyzir](https://clawhub.ai/user/kennyzir)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and site operators use this skill to check directory submission pages and batch submit website metadata to AI tool, developer, and SEO directories for backlink campaigns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit website and contact details to third-party directory sites, which may create public or irreversible listings.

Mitigation: Review the directory list and all site/contact information before running submissions, and avoid sensitive personal email addresses.

Risk: Submission controls are limited, so automated runs may target paid, login-gated, or unsuitable directories.

Mitigation: Run batch_submit.py with --check-only first and review the detected status for each directory before submitting.

Risk: quick_submit.py contains hardcoded sample data and destinations.

Mitigation: Edit quick_submit.py data and URL values before execution, or use batch_submit.py with explicit reviewed inputs.

Risk: The scripts install and run browser automation and HTTP dependencies.

Mitigation: Install dependencies in an isolated environment before running the skill.

## Reference(s):

- [Directory targets list](artifact/references/directories.txt)
- [Targets README](artifact/targets/README.md)
- [ClawHub skill page](https://clawhub.ai/kennyzir/skills/seo-backlink-submitter)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes timestamped batch_result_*.json files when batch_submit.py runs.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
