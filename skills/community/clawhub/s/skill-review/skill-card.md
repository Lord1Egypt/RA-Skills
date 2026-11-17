## Description:

Scrape ClawHub skill pages for Security Scan, Runtime Requirements, and Comments across local skills, then write a markdown report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odrobnik](https://clawhub.ai/user/odrobnik)

### License/Terms of Use:


## Use Case:

Developers and skill maintainers use this skill to review ClawHub security scan results, runtime requirements, and comments for local ClawHub skills and collect the results in a report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads all local skills in the configured skills directory.

Mitigation: Run it only against directories you intend to audit and review the selected --skills-dir before execution.

Risk: The skill contacts ClawHub and VirusTotal and may use a VirusTotal API key from the environment or ~/.openclaw/.env.

Mitigation: Use it in an approved network environment and provide only an API key intended for this audit workflow.

Risk: Bundled suppressions can change how warning statuses are reported.

Mitigation: Review suppressions.json before relying on the generated report.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/odrobnik/skills/skill-review)
- [Skill Homepage](https://github.com/odrobnik/skill-review-skill)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown report or JSON report with command-line instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write reports under /tmp and cache VirusTotal results when configured.]

## Skill Version(s):

0.2.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
