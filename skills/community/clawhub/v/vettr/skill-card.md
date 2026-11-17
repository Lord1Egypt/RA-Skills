## Description:

Static analysis security scanner for third-party OpenClaw skills. Detects eval/spawn risks, malicious dependencies, typosquatting, and prompt injection patterns before installation. Use when vetting skills from ClawHub or untrusted sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[britrik](https://clawhub.ai/user/britrik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to evaluate third-party OpenClaw skills before installation. It reports static-analysis findings for risky code execution, shell use, dependency issues, typosquatting, prompt-injection patterns, and related metadata concerns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target skills can include ignore-file rules that hide files from local analysis and make scan results incomplete or misleading.

Mitigation: Treat results as one input, inspect ignore rules, and manually review high-risk skills before relying on a pass or fail outcome.

Risk: Remote URL vetting downloads untrusted content and can reach unintended network targets.

Mitigation: Run remote vetting only in a disposable or network-restricted environment, especially for untrusted URLs.

Risk: npm dependencies and external binaries used during remote vetting are part of the trust boundary.

Mitigation: Verify the runtime environment, dependencies, and git, curl, tar, and clawhub binaries before using remote vetting workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/britrik/skills/vettr)
- [Project homepage](https://github.com/britrik/skill-vettr)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style text with risk summaries, findings, recommendations, usage messages, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are heuristic and should be reviewed before acting on installation decisions.]

## Skill Version(s):

2.0.4 (source: server release evidence; artifact frontmatter and package.json show 2.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
