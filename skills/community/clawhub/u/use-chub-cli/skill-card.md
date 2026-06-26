## Description: <br>
Use the Context Hub chub CLI to fetch current third-party SDK, API, and cloud-service documentation before writing, modifying, or reviewing integration code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kshern](https://clawhub.ai/user/kshern) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to look up current third-party SDK, API, and cloud-service documentation with the chub CLI before implementing or reviewing integration code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a local or repository-provided chub executable, which may not be trustworthy in every environment. <br>
Mitigation: Verify that the chub executable or repository-local ./cli/bin/chub fallback comes from a trusted source before use. <br>
Risk: Annotations or feedback could accidentally include secrets or confidential project details. <br>
Mitigation: Do not store secrets, credentials, or confidential details in chub annotations or feedback. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kshern/use-chub-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CLI command selections, documentation lookup results, integration guidance, code examples, and cautions about trusted chub executables and sensitive annotations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
