## Description:

Clawhub Guard provides CLI-style commands for browsing, searching, auditing, and installing ClawHub marketplace skills with lightweight risk hints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangxianzhan](https://clawhub.ai/user/huangxianzhan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Clawhub Guard to scan or search ClawHub marketplace listings, review simple risk hints, audit installed skills for updates, and install selected skills after manual inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises safety checks that evidence indicates it does not actually perform.

Mitigation: Treat its ratings as convenience hints only and independently inspect packages before trusting or installing them.

Risk: The install command can install marketplace skills.

Mitigation: Use the install command only for sources you already trust after manual review.

## Reference(s):

- [Clawhub Guard marketplace listing](https://clawhub.ai/huangxianzhan/skills/skill-market-scanner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Console text and Markdown-style recommendations with command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke the ClawHub CLI to inspect or install marketplace skills.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
