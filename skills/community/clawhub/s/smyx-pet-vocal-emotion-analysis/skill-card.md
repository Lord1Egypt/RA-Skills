## Description: <br>
Analyzes uploaded cat or dog vocal audio or video through a cloud API to return pet emotion, intent, confidence, and interaction guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and pet-care assistants use this skill to analyze pet vocal media, interpret likely emotions or behavioral intent, and retrieve prior cloud-hosted analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads pet media and user-linked identifiers to cloud services. <br>
Mitigation: Disclose what media and identifiers are sent, which service receives them, and the retention policy before use. <br>
Risk: Server security evidence says the implementation includes broader video, health, history, and account-management behavior beyond the pet vocal-analysis claim. <br>
Mitigation: Require publisher clarification and narrow the deployed skill to pet audio/video analysis before installation. <br>
Risk: The security summary flags identity handling, token persistence, and generic CRUD or delete helpers. <br>
Mitigation: Remove or isolate account-management and token-persistence helpers, and run only with least-privilege credentials. <br>
Risk: The security guidance identifies an invalid yaml dependency. <br>
Mitigation: Replace it with a legitimate YAML package and verify dependencies before installing. <br>


## Reference(s): <br>
- [API interface documentation](references/api_doc.md) <br>
- [ClawHub skill listing](https://clawhub.ai/smyx-sunjinhui/smyx-pet-vocal-emotion-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown reports or JSON analysis output, with shell command examples for invocation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [History queries may include Markdown tables with links to cloud-hosted report pages.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; skill frontmatter says 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
