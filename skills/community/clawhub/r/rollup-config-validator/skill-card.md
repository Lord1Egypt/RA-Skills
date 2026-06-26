## Description: <br>
Validate Rollup config files (rollup.config.js/mjs/ts) for output format conflicts, plugin ordering issues, deprecated options, and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and build engineers use this skill to validate JSON representations of Rollup configuration objects, audit build pipelines, catch configuration errors, and get CI-friendly findings before release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The validator handles JSON or JSONC-style Rollup configuration data reliably, but it is not a complete security review of executable rollup.config.js, .mjs, or .ts files. <br>
Mitigation: Export or convert Rollup config objects to JSON before validation, and review executable configuration code separately before trusting build behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/rollup-config-validator) <br>
- [Publisher profile](https://clawhub.ai/user/charlie-morrison) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON examples, and validator findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports text, JSON, and summary validator output with CI-friendly exit codes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
