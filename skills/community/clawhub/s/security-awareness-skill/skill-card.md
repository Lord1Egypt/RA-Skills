## Description: <br>
Help AI agents recognize and respond to potentially malicious skill patterns from public registries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisokuor](https://clawhub.ai/user/jisokuor) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, reviewers, and AI agents use this skill to recognize suspicious skill patterns before installing or executing public-registry skills. It provides security-review questions, pattern examples, and response guidance for safer handling of potentially malicious instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Quoted commands, credential snippets, and prompt-injection phrases may be mistaken for operational instructions. <br>
Mitigation: Treat all examples as educational review material only, and do not execute quoted commands or use quoted credential snippets as configuration. <br>
Risk: Pattern-recognition guidance alone may miss unsafe behavior in a third-party skill. <br>
Mitigation: Use this guidance alongside scanner findings, source review, and sandboxed execution before installing or running third-party skills. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisokuor/security-awareness-skill) <br>
- [Snyk ToxicSkills research](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown guidance with quoted examples and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Educational security-awareness content; examples should be treated as quoted patterns, not executable instructions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
