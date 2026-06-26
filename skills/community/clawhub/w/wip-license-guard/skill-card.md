## Description: <br>
License compliance for your own repos. Ensures correct copyright headers, dual-license blocks, and LICENSE files across all source files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to audit local repositories for expected license files, copyright lines, CLA files, and README license sections. It can also guide or run fix workflows when repository license metadata needs to be standardized before release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fix modes can rewrite LICENSE, CLA, and README files in local repositories. <br>
Mitigation: Run audit or --dry-run first, use --fix only on a clean branch, and review git diffs before committing. <br>
Risk: The readme-license --fix workflow can affect every detected repository when pointed at a broad parent directory. <br>
Mitigation: Run it against a specific repository or carefully scoped directory unless broad README license updates are intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/parkertoddbrooks/wip-license-guard) <br>
- [Project Homepage](https://github.com/wipcomputer/wip-ai-devops-toolbox) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose audit, dry-run, or fix commands for local repository license compliance.] <br>

## Skill Version(s): <br>
1.9.72 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
