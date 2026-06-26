## Description: <br>
Spec-Kit SDD guides agents through GitHub Spec-Kit based spec-driven development workflows, including project initialization, constitution management, specifications, plans, task breakdowns, implementation, analysis, extension management, and Paperclip issue handoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[james-code-hash](https://clawhub.ai/user/james-code-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run a structured Spec-Kit SDD workflow from project setup through specification, planning, tasks, implementation, and consistency review. It also provides operational guidance for Paperclip issue reassignment when coordinating work across agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paperclip PATCH/POST commands or the helper script can change issue ownership or add comments. <br>
Mitigation: Confirm the issue ID, assignee, API URL, and credentials before running Paperclip commands or helper scripts. <br>
Risk: The workflow may propose specification, plan, task, or implementation changes that drift from the project constitution or current code. <br>
Mitigation: Review generated artifacts against the project constitution and run the analyze and checklist steps before implementation or release. <br>


## Reference(s): <br>
- [Constitution Management Guide](references/constitution-guide.md) <br>
- [GitHub Spec-Kit repository](https://github.com/github/spec-kit) <br>
- [GitHub blog: Spec-driven development with AI](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) <br>
- [Addy Osmani: How to write a good software design doc](https://addyosmani.com/blog/good-spec/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline command examples, file paths, tables, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose project files, specification artifacts, implementation tasks, API calls, and Paperclip reassignment commands for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
