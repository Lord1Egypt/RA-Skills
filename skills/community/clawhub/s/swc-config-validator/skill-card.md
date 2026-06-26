## Description: <br>
Validate SWC config files (.swcrc, package.json#swc) for parser settings, transform conflicts, module type issues, and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to validate .swcrc and package.json SWC configuration before build or CI use, including parser settings, transform conflicts, module output, minification settings, and best-practice warnings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The validator reads whichever local file path the user provides. <br>
Mitigation: Run it only against intended SWC configuration files and avoid passing unrelated sensitive files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/swc-config-validator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional text, JSON, or summary validator output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports CI-friendly exit codes and strict mode where warnings become errors.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
