## Description: <br>
Vitest Testing provides Vitest testing framework patterns and best practices for writing tests, configuring vitest.config, mocking with vi.mock and vi.fn, using snapshots, and setting up coverage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to draft, review, and improve Vitest unit and integration tests, test configuration, mocks, snapshots, coverage setup, and async matcher usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or suggested tests may change assertions, fixtures, or snapshots in unintended ways. <br>
Mitigation: Review generated test files and snapshot changes before committing them. <br>
Risk: Running project test commands can execute code from the target repository. <br>
Mitigation: Run tests only in a trusted workspace and use the same command that CI uses from the package or workspace root. <br>
Risk: Vitest resolves or rejects matchers without await can create false-positive tests. <br>
Mitigation: Check that every resolves or rejects matcher is prefixed with await before accepting changes. <br>


## Reference(s): <br>
- [Mocking Patterns](references/mocking.md) <br>
- [Configuration](references/config.md) <br>
- [Common Patterns](references/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript code examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no direct API calls or tool integrations.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
