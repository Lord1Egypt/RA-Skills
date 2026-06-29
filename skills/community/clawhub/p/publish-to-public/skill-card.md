## Description: <br>
Generic rebrand pipeline. Deterministic, idempotent, byte-to-byte. Strip jargon, fix paths, regenerate manifests, validate. Use when preparing internal code for public release, marketplace publication, or open-sourcing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to prepare internal code for public release, marketplace publication, open-sourcing, or CI checks by removing configured jargon, fixing path references, regenerating manifests, and producing an audit report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and rewrites a whole source tree into a destination, so an incorrect source, destination, or pattern configuration could alter more files than intended. <br>
Mitigation: Run it first with --dry-run, use a clean destination directory, and review the generated audit before relying on the output. <br>
Risk: Optional validation can execute local Python code from the processed project. <br>
Mitigation: Do not pass --validator or run validation/tests on untrusted projects unless the run is isolated in a container or virtual machine. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/publish-to-public) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, Python API examples, YAML/JSON configuration examples, and JSON audit output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes source trees into destination trees; dry-run mode previews changes, and optional validation can run local tests or a custom validator.] <br>

## Skill Version(s): <br>
0.1.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
