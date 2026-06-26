## Description: <br>
Universal agent workspace compatibility and update engine for importing upstream agent frameworks, analyzing changes, classifying portability, and generating adapted output for agent runtimes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aggie-security](https://clawhub.ai/user/aggie-security) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use uStack to track upstream agent-native repositories, analyze framework changes, classify portability, and publish update reports for local agent runtime compatibility work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: uStack clones arbitrary Git repositories provided by the user and writes analysis artifacts under .ustack. <br>
Mitigation: Use trusted repository URLs, review generated .ustack artifacts before publishing them, and avoid untrusted repositories until git shell-interpolation hardening is complete. <br>


## Reference(s): <br>
- [uStack README](README.md) <br>
- [uStack changelog](CHANGELOG.md) <br>
- [uStack ClawHub release page](https://clawhub.ai/aggie-security/ustack) <br>
- [gstack upstream repository](https://github.com/garrytan/gstack) <br>
- [AGI.security](https://agi.security) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON files with CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local .ustack manifests, analysis reports, and website-ready update pages.] <br>

## Skill Version(s): <br>
0.1.0 (source: package.json, CHANGELOG, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
