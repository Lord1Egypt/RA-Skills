## Description: <br>
Policy benchmarking runner for MCP security policies that runs attack suites against protect-mcp policy packs and produces signed receipts and badges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomjwxf](https://clawhub.ai/user/tomjwxf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to benchmark protect-mcp policies by running deterministic attack suites and checking whether the policies block or allow the expected cases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recommended install command uses unpinned @latest npm packages that can change over time and execute package code during installation or use. <br>
Mitigation: Install only trusted package versions, prefer pinning versions, and run the benchmark in a disposable project environment. <br>


## Reference(s): <br>
- [ScopeBlind Red Team npm package](https://npmjs.com/package/@scopeblind/red-team) <br>
- [ScopeBlind Red Team documentation](https://scopeblind.com/docs/red-team) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, markdown] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent to run an external benchmark CLI that produces receipts and badges.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
