## Description: <br>
Skill Router is a centralized index and router that helps an agent identify installed skills, load matching specialized skills, and report skill usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yunzhouli-hub](https://clawhub.ai/user/yunzhouli-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to keep an installed skill set discoverable, route user requests to relevant skills, and make skill usage visible after responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill attempts to act as an always-on router for every question, which can influence responses beyond narrow skill-routing tasks. <br>
Mitigation: Install it only when a global router is intended, and narrow the activation language if only explicit skill-routing behavior is desired. <br>
Risk: Generated skill indexes and usage reports may expose local skill names, descriptions, or usage patterns more broadly than expected. <br>
Mitigation: Review generated SKILL.md content before sharing or deployment, and avoid publishing indexes that reveal sensitive local skill metadata. <br>
Risk: Automatic routing may load extra skills that are unnecessary for a task. <br>
Mitigation: Review routing rules and adjust match criteria so skills load only for clear matches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yunzhouli-hub/skill-router-hub) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/yunzhouli-hub) <br>
- [Anthropic skills repository](https://github.com/anthropics/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated skill-index content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate or update a SKILL.md index from local installed-skill metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
