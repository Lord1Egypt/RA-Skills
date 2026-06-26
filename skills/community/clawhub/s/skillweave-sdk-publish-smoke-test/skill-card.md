## Description: <br>
Verifies ClawHub publish flows from the TypeScript client with a non-trivial SKILL.md body. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nashirjamali](https://clawhub.ai/user/nashirjamali) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill as a repeatable checklist for validating Skillweave or ClawHub skill publishing from a TypeScript client, including API payload construction, publish verification, and common validation failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing with a real namespace or production slug can create or update registry entries unintentionally. <br>
Mitigation: Use a test slug or namespace when validating publish flows, and confirm slug policy before republishing or undeleting skills. <br>
Risk: The publishing workflow requires CLAWHUB_TOKEN, which could be exposed if handled carelessly. <br>
Mitigation: Load the token from a local environment file or secret store, keep it out of version control, and use least-privilege publish access. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration] <br>
**Output Format:** [Markdown with a TypeScript code block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only checklist; no hidden executable code is included in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
