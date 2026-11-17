## Description:

Benchmark ClawHub skills: performance, correctness, documentation quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itspremkumar](https://clawhub.ai/user/itspremkumar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, and reviewers use this skill to score ClawHub/OpenClaw/Hermes skill folders for structure, documentation, safety, self-test coverage, and overall quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package documentation includes a curl command for fetching unpinned remote code.

Mitigation: Prefer the bundled skill_benchmark.py from the reviewed package, or use a pinned release with a verified hash before execution.

Risk: The verification harness can execute candidate project code during dynamic checks.

Mitigation: Run dynamic tests only in a disposable, secret-free sandbox with restricted filesystem and network access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/itspremkumar/skills/skill-benchmark)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain text or JSON benchmark report with grade, numeric score, and issue list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs offline with Python 3.8+; scoring is heuristic and should be reviewed before release decisions.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
