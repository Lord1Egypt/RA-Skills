## Description: <br>
Improve reusable agent workflows with reflective experiments, value checks, and local pattern memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to improve repeated workflows by recording local experiment notes, testing one behavior change at a time, and promoting only proven patterns into stable memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local notes may capture sensitive workflow details if the user lets the agent save too much context. <br>
Mitigation: Review ~/self-evolving/ periodically, avoid storing secrets or sensitive personal or business details, and pause or opt out of memory updates when needed. <br>
Risk: Unreviewed behavior changes could make the agent less reliable or change workflows without clear value. <br>
Mitigation: Use one small experiment at a time, require explicit evidence across comparable uses before promotion, and discard changes that add churn or weaken reliability. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/self-evolving) <br>
- [Skill homepage](https://clawic.com/skills/self-evolving) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance and local memory templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains concise local notes under ~/self-evolving/ when the user allows persistent writes.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
