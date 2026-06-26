## Description: <br>
Distribute iOS and macOS beta builds with TestFlight, tester management, and CI/CD automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and release engineers use this skill to prepare and automate TestFlight distribution for iOS and macOS beta builds, including App Store Connect setup, tester groups, build uploads, CI/CD examples, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Apple release credentials, certificates, and API keys may be exposed or over-privileged during CI/CD automation. <br>
Mitigation: Use least-privilege App Store Connect credentials, store secrets in CI secret storage or Keychain, and prefer ephemeral macOS runners. <br>
Risk: External TestFlight distribution or beta review submission may happen before the release is ready. <br>
Mitigation: Require explicit approval before enabling external distribution or submitting a build for beta review. <br>
Risk: Generated keychains, provisioning profiles, or credential files may remain on runners after upload. <br>
Mitigation: Add cleanup steps for generated keychains, provisioning profiles, and temporary credential files. <br>


## Reference(s): <br>
- [TestFlight skill page](https://clawhub.ai/ivangdavila/testflight) <br>
- [Skill homepage](https://clawic.com/skills/testflight) <br>
- [App Store Connect](https://appstoreconnect.apple.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bash, YAML, JSON, Ruby, and XML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Covers macOS-based TestFlight release workflows and Apple credential handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
