## Description: <br>
Scaffold the standard ai/ directory structure in any repo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering agents use this skill to initialize a standard ai/ working directory with plans, notes, product docs, dev updates, todos, and holding areas for sorting or archiving existing files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool creates and reorganizes files in the target repository, including moving an existing ai/ directory into ai/_sort/ai_old/. <br>
Mitigation: Run with --dry-run first, inspect the target path, and use --yes only when the planned changes are understood. <br>
Risk: The generated ai/ content may contain private planning notes or working context that should not be published. <br>
Mitigation: Do not rely on generated privacy wording alone; confirm repository ignore rules, release scripts, and deployment packaging exclude ai/ when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/parkertoddbrooks/wip-repo-init) <br>
- [Project homepage](https://github.com/wipcomputer/wip-ai-devops-toolbox) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and generated repository files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or reorganizes a local ai/ directory; supports dry-run and confirmation controls.] <br>

## Skill Version(s): <br>
1.9.72 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
