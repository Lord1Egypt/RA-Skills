## Description: <br>
Skill Firewall is a defensive instruction skill that helps agents review and rewrite third-party skills before saving them to reduce prompt-injection risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mkhaytman87](https://clawhub.ai/user/mkhaytman87) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill when evaluating external skills from ClawHub, skills.sh, GitHub, or similar sources. It guides the agent to identify the external skill's legitimate purpose, create a clean rewrite, and request user approval before saving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may intervene broadly when external skills are discussed. <br>
Mitigation: Review the generated Skill Firewall report and approve only rewritten skill content that matches the intended external skill purpose. <br>
Risk: A rewritten skill could omit useful behavior or preserve incorrect guidance from the external source. <br>
Mitigation: Compare the identified purpose with the clean rewrite before saving, and request revisions when the rewrite does not match the expected scope. <br>


## Reference(s): <br>
- [Skill Firewall ClawHub page](https://clawhub.ai/mkhaytman87/skill-firewall) <br>
- [Skill Firewall homepage](https://github.com/openclaw/skill-firewall) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance and rewritten skill content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user approval before saving rewritten skill content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
