## Description:

Distribute iOS and macOS beta builds with TestFlight, tester management, and CI/CD automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and release engineers use this skill to prepare TestFlight beta distribution, manage tester groups, upload iOS or macOS builds, and integrate Fastlane or CI/CD release workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CI snippets may expose Apple signing credentials through weak temporary files or an empty-password keychain.

Mitigation: Use isolated ephemeral runners, generate a non-empty temporary keychain password, restrict file permissions, and delete temporary credential files and keychains in an always-run cleanup step.

Risk: Release automation may use broader App Store Connect access than necessary.

Mitigation: Use the least-privileged App Store Connect role that supports the release process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/testflight)
- [Skill homepage](https://clawic.com/skills/testflight)
- [App Store Connect](https://appstoreconnect.apple.com)
- [CI/CD automation](artifact/ci-cd.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML, JSON, Ruby, XML, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides macOS-focused TestFlight release guidance; metadata lists Darwin support and no required local binaries.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
