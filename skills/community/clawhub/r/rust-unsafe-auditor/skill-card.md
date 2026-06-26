## Description: <br>
Audit Rust code for unsafe block usage, safety invariants, FFI boundaries, raw pointer operations, Send/Sync implementations, and unsound abstractions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to audit Rust crates for unsafe-code soundness, FFI boundary issues, raw pointer hazards, safety documentation gaps, and unsafe reduction opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit output may include private source details from the reviewed repository. <br>
Mitigation: Run the skill from the intended project directory and treat generated audit output as sensitive project information. <br>
Risk: Optional cargo commands may build or test code from the local repository. <br>
Mitigation: Approve cargo commands only when the repository is trusted enough to build or test locally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/rust-unsafe-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown audit report with shell command snippets and tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include audit summaries, critical findings, documentation gaps, and recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
