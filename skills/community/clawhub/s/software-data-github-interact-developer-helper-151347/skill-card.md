## Description: <br>
Helps users plan, implement, verify, and document GitHub-style developer workflows on ClawHub, including bug fixing, setup hardening, reliability improvements, and adjacent skill creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyro-ma](https://clawhub.ai/user/kyro-ma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, skill authors, maintainers, and teams use this skill to turn GitHub-style workflow requests into concrete artifacts such as plans, checklists, implementation guidance, code changes, and verification notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad implicit invocation may select the skill for unrelated software questions. <br>
Mitigation: Review trigger wording before deployment and prefer explicit invocation when narrower routing is required. <br>
Risk: Generated workflow, code, or shell-command guidance may be incorrect for a user's local repository or environment. <br>
Mitigation: Review proposed changes and run the included validation or test commands before applying them to important projects. <br>


## Reference(s): <br>
- [Requirement Plan](references/requirement-plan.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/software-data-github-interact-developer-helper-151347) <br>
- [GitHub Workflow Demand Signal](https://clawhub.ai/skills/github) <br>
- [OpenChamber Issue 1733](https://github.com/openchamber/openchamber/issues/1733) <br>
- [RN CI Workflow Builder Issue 64](https://github.com/mobile-dev-ci/rn-ci-workflow-builder/issues/64) <br>
- [Motrix Next Extension Issue 43](https://github.com/AnInsomniacy/motrix-next-extension/issues/43) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with optional code blocks, shell commands, checklists, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes assumptions, validation notes, and remaining risks when relevant.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
