## Description: <br>
Query DeFi yield opportunities across chains using the yieldsllama CLI, powered by the DeFi Llama API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lolieatapple](https://clawhub.ai/user/lolieatapple) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to install and run a third-party CLI that compares DeFi yield pools by chain, asset, APY, TVL, and exposure type, then summarize the results with yield-risk context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow asks users to build and run a third-party Rust CLI. <br>
Mitigation: Review the repository before installation, pin a known commit, and install to a user-local path when possible. <br>
Risk: The CLI uses local .env and data.json files in the current working directory. <br>
Mitigation: Run commands from a dedicated directory so generated configuration and cached data do not affect another project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lolieatapple/yieldsllama) <br>
- [Rust installation tools](https://www.rust-lang.org/tools/install) <br>
- [DeFi Llama yields API endpoint](https://yields.llama.fi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and comparison tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or refresh local .env and data.json files when following the documented CLI workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
