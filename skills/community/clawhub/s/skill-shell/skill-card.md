## Description: <br>
Evaluate external skills before installation and decide whether to install, reject, or absorb only the useful ideas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[G-Hanasq](https://clawhub.ai/user/G-Hanasq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to perform read-only intake reviews of external ClawHub or GitHub skills before installation. It helps classify a candidate skill, identify static and dynamic validation needs, and recommend installation, rejection, postponement, or absorbing useful ideas only. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can encourage agents to carry ideas from untrusted external skills into persistent workflow or memory files. <br>
Mitigation: Use it for read-only review by default, require explicit user approval before any persistent file updates, and inspect the exact proposed changes before writing them. <br>
Risk: A candidate skill may require runtime validation beyond static file review before it is safe or useful. <br>
Mitigation: Treat static review and dynamic validation as separate steps, and only call a skill fully ready after the required environment level has been tested. <br>


## Reference(s): <br>
- [Skill Intake Checklist](references/checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/G-Hanasq/skill-shell) <br>
- [Publisher Profile](https://clawhub.ai/user/G-Hanasq) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Markdown] <br>
**Output Format:** [Markdown report with recommendation labels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces skill review conclusions, risk notes, fit assessment, and installation recommendations.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
