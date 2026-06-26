## Description: <br>
Swiss-army knife for JSON files that pretty-prints, validates, minifies, sorts keys, and queries with dot-notation paths using zero dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[claudiodrusus](https://clawhub.ai/user/claudiodrusus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to format, validate, minify, sort, and query JSON data from local files or stdin while working in shell pipelines or code repositories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The utility reads JSON files or stdin and can write transformed JSON to a user-selected path. <br>
Mitigation: Run it only on intended inputs, avoid sensitive files unless needed, and review output paths before using --output. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/claudiodrusus/skill-3) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands] <br>
**Output Format:** [JSON or plain text from a local Python CLI; Markdown may be used for agent guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can read JSON from a file or stdin and optionally write transformed JSON to a specified output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
