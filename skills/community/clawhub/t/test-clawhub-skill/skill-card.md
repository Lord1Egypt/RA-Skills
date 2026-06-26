## Description: <br>
Tests ClawHub CLI publishing by validating publish command parameter handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forealmy](https://clawhub.ai/user/forealmy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to smoke-test ClawHub CLI publish argument handling for name, version, tags, and changelog fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact is a placeholder smoke test rather than a comprehensive CLI test suite. <br>
Mitigation: Use it only to validate basic publish-argument handling and rely on separate tests for full CLI behavior. <br>
Risk: The included script executes local Python code. <br>
Mitigation: Review the short script before running it; current server security evidence reports no credentials, network access, elevated permissions, or persistent behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/forealmy/test-clawhub-skill) <br>
- [README](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code] <br>
**Output Format:** [Markdown with inline shell commands and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a minimal Python script that prints a test message.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
