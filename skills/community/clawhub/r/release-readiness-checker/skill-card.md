## Description:

Runs a pre-release audit for software projects, checking release metadata, tests, dependencies, secrets, CI status, documentation, and Git state before producing a go/no-go report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill before tagging or shipping a release to identify blockers such as missing tests, critical vulnerabilities, committed secrets, stale documentation, or uncommitted changes. It provides advisory release readiness guidance rather than replacing CI, security review, or project-specific approval gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's output is advisory and may miss project-specific release requirements or produce false positives during pattern-based checks.

Mitigation: Treat the report as a review aid, run the real test suite and CI enforcement separately, and manually review flagged findings before release decisions.

Risk: Some checks may query local npm or GitHub status through installed tools and can depend on network access or local authentication.

Mitigation: Avoid network-dependent checks in sensitive offline environments unless approved, and confirm that tools such as gh are configured before relying on CI status output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/release-readiness-checker)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Human-readable release readiness reports, markdown checklists, optional JSON summaries, and suggested shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can report GO, CAUTION, or NO-GO states with blockers, warnings, passing checks, and CI-oriented exit code guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
