## Description: <br>
Create new skills, modify and improve existing skills, and measure skill performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhanggd6](https://clawhub.ai/user/zhanggd6) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agent builders use this skill to create, update, evaluate, benchmark, and package agent skills. It helps teams define skill behavior, run comparative evaluations, review results, and iterate based on quantitative and qualitative feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or modify other skills and supporting files. <br>
Mitigation: Review generated skill content, diffs, and packaged artifacts before deploying or sharing them. <br>
Risk: Evaluation workflows may run Claude CLI evaluations using the user's existing session and may include prompt or file content in local reports. <br>
Mitigation: Do not include secrets or proprietary content in eval prompts or skill files unless that content is approved for the configured Claude environment and local report storage. <br>
Risk: The review viewer can start a local web server and write feedback or report files. <br>
Mitigation: Prefer static report generation when possible and avoid ports used by important local services. <br>


## Reference(s): <br>
- [Skill Creator ClawHub Release](https://clawhub.ai/zhanggd6/skill-creator2) <br>
- [Skill Creator JSON Schemas](references/schemas.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, shell command snippets, and local files for skills, evaluations, reports, and review pages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify skill files, eval metadata, benchmark reports, package artifacts, and static or locally served HTML review pages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
