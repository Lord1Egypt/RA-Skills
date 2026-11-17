## Description:

Tongyong Shenhe helps agents configure and run rule-based content moderation workflows for d.php admin sites, with optional API-assisted review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wulooongcha](https://clawhub.ai/user/wulooongcha)

### License/Terms of Use:

MIT-0

## Use Case:

Internal moderation operators and developers use this skill to configure site credentials and rules, test moderation decisions in dry-run or fetch-only mode, and submit decisions for compatible d.php admin sites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses administrator credentials and a reusable TOTP seed for live moderation workflows.

Mitigation: Install only for approved internal moderation workflows, use a least-privileged service account, and protect config files with strict permissions.

Risk: Live mode can submit moderation approvals or rejections to configured sites.

Mitigation: Run dry-run or fetch-only first, review decisions, and enable live submission only after site-specific rules are validated.

Risk: Optional API-assisted review can send submitted content to a configured external moderation endpoint.

Mitigation: Verify or replace the API endpoint before setting an API key and confirm that content sharing is approved for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wulooongcha/skills/tongyong-shenhe)
- [Usage guide](artifact/USAGE.md)
- [Deployment guide](artifact/DEPLOY.md)
- [Example configuration](artifact/config.example.json)
- [Default moderation rules](artifact/rules.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown instructions with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate pending_review.json in fetch-only mode and consume decisions.json in submit mode.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
