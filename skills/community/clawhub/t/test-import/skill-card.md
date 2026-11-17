## Description:

Publishes a local skill to ClawHub using command-line or Python API inputs for slug, name, version, path, and optional changelog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuhaichao87](https://clawhub.ai/user/wuhaichao87)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to publish local skill directories to ClawHub by providing release metadata and a source path. It supports both command-line use and Python API invocation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports a hardcoded publishing token in the skill.

Mitigation: Do not install or run this version with the embedded token present; revoke the exposed token and replace it with user-provided credentials.

Risk: The release evidence reports that the skill uploads matching local source and text files to ClawHub without strong user review controls.

Mitigation: Review the target directory before use and add a dry-run or confirmation step before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuhaichao87/skills/test-import)
- [Publisher profile](https://clawhub.ai/user/wuhaichao87)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke ClawHub API calls and upload matching local source or text files when executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
