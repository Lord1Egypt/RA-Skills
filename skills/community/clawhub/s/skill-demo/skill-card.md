## Description: <br>
Minimal TypeScript hello-world skill that demonstrates bundling TS code, a Node dependency, and package.json instructions for use and publication on Clawdhub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whgreate](https://clawhub.ai/user/whgreate) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill as a minimal TypeScript example for installing npm dependencies, running a hello-world script, importing a greeting function, and testing simple deterministic embedding helpers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the demo runs npm dependency resolution for third-party packages. <br>
Mitigation: Review package.json before installation and install dependencies only from the intended skill directory. <br>
Risk: The fake embedding helper is deterministic demo logic and is not suitable for production semantic search. <br>
Mitigation: Use it only for wiring, tests, and examples; replace it with a production embedding implementation for real retrieval or search workflows. <br>


## Reference(s): <br>
- [README Usage](references/README-usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown usage guidance with TypeScript code and shell command examples; demo scripts produce strings and numeric arrays.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes npm package metadata and local TypeScript example scripts.] <br>

## Skill Version(s): <br>
0.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
