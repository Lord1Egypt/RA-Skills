## Description:

Release Gate Audit helps agents decide whether a repository or artifact is ready to publish by auditing tracked files and git history for credentials, organization-internal information, PII, and local-only files, then guiding remediation verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, release managers, and compliance reviewers use this skill before open-sourcing, externally sharing, or releasing code and skill artifacts. It focuses review on the public surface of a git repository, separates findings by remediation path, and helps verify that fixes were completed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports confirmed flaws that could read outside the target repository.

Mitigation: Run the skill under a low-privilege account and review it before installing it as a release gate.

Risk: The security review reports that the skill could miss real secrets while presenting release-gate results.

Mitigation: Use results as advisory until symlink boundary checks, content-bound baseline fingerprints, and long-line scanning are fixed.

Risk: Organization term files can contain sensitive internal identifiers.

Mitigation: Keep organization term files out of published repositories and manage them locally or through approved internal channels.

Risk: A passing report may be mistaken for proof that a repository is safe to publish.

Mitigation: Require human review of findings, provenance, and release scope before publication.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tencent-adm/skills/release-gate-audit)
- [Threat Categories](references/threat-categories.md)
- [False Positive Playbook](references/false-positive-playbook.md)
- [Organization Terms Template](assets/org-terms.txt)
- [Self-audit Baseline Example](assets/self-audit-baseline.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or terminal text with optional JSON audit reports and remediation comparison output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include release-gate verdicts, categorized findings, baseline guidance, and credential revocation checklists.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
