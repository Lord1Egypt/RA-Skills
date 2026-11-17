## Description:

Sentry.io error monitoring via sentry-cli. Use when working with Sentry releases, source maps, dSYMs, events, or issue management. Covers authentication, release workflows, deploy tracking, and debug file uploads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iahmadzain](https://clawhub.ai/user/iahmadzain)

### License/Terms of Use:


## Use Case:

Developers and release engineers use this skill to operate Sentry CLI workflows for authentication, release creation, deploy tracking, source map uploads, debug file uploads, event testing, issue management, and monitor check-ins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes an installation pattern that can execute mutable remote code on a user's machine.

Mitigation: Prefer a trusted package manager or a pinned, verified release instead of running the pipe-to-shell command.

Risk: Sentry authentication tokens can grant access to organization or project data and release operations.

Mitigation: Use least-privilege Sentry tokens and store them in CI secrets or environment configuration rather than committing credentials.

Risk: CI examples may rely on mutable third-party actions or dependencies when copied into production pipelines.

Mitigation: Pin CI actions and dependencies when adapting the examples.

## Reference(s):

- [Sentry CLI installer](https://sentry.io/get-cli/)
- [ClawHub skill page](https://clawhub.ai/iahmadzain/skills/sentry-cli)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash, INI, and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Sentry CLI command examples and token/configuration guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
