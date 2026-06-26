## Description: <br>
One-click initialization of an AI-driven unit testing environment for frontend projects, including React, Vue, pure TypeScript, and Next.js projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hibehero](https://clawhub.ai/user/hibehero) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to initialize Vitest-based frontend unit testing, generate test configuration files, install test dependencies, add Claude Code test-generation commands, and integrate a Husky pre-commit test guard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify dependency manifests, lockfiles, Vitest/MSW configuration, .claude command files, and Husky pre-commit hooks in the target project. <br>
Mitigation: Review generated files, dependency changes, and hook changes before committing them. <br>
Risk: Automatic test generation can send selected repository source context to Claude Code when command workflows are invoked. <br>
Mitigation: Keep AUTO_GEN_TEST unset unless automatic generation is intended, and run /gen-unit-test only on paths that are appropriate to share with the configured agent. <br>


## Reference(s): <br>
- [AI Unit Test Generation Rules](references/gen-unit-test-prompt.md) <br>
- [Test Failure Repair Rules](references/fix-test-prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, generated configuration files, scripts, and Claude Code command templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local project changes for Vitest, Testing Library, MSW, Husky, and .claude command workflows.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
