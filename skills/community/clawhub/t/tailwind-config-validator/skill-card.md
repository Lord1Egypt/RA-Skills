## Description: <br>
Validate JSON-exported Tailwind CSS configuration files for structural issues, content path problems, theme misconfiguration, and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit Tailwind CSS configuration before production builds or CI enforcement. It helps identify content path, theme, dark mode, plugin, and best-practice issues from a JSON-exported Tailwind config. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exporting a Tailwind JavaScript configuration with Node can execute code from the target project. <br>
Mitigation: Run the export command only in Tailwind projects you trust, or isolate the project before generating the JSON config. <br>
Risk: Server-resolved GitHub import provenance is unavailable for this version. <br>
Mitigation: Review the included source files before adoption when publisher provenance is important. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance plus validator output in text, JSON, or summary format] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The validator can exit nonzero when errors are found, or when warnings are present in strict mode.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
