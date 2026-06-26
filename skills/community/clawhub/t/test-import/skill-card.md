## Description: <br>
Publishes a local skill to ClawHub using command-line or Python API with specified slug, name, version, path, and optional changelog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuhaichao87](https://clawhub.ai/user/wuhaichao87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to publish local skill directories to ClawHub from the command line or from Python, supplying release metadata and an optional changelog. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill ships with an embedded bearer token. <br>
Mitigation: Treat the token as exposed, rotate or revoke it, and require users to provide their own credential at runtime. <br>
Risk: The skill can upload local skill files without clear pre-upload review. <br>
Mitigation: Run it only on non-sensitive skill directories after listing and confirming exactly which files will be uploaded. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuhaichao87/test-import) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include slug, display name, version, local skill path, and optional changelog values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
