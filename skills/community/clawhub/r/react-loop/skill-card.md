## Description: <br>
Solve complex problems by interleaving reasoning with actions, observing results, and using those observations to guide the next step. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simoncatbot](https://clawhub.ai/user/simoncatbot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill to structure multi-step research, debugging, data analysis, and tool-heavy workflows as repeated thought, action, and observation cycles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can guide agents toward broad tool use, including irreversible actions such as database writes, migrations, deployments, external messages, or issue creation. <br>
Mitigation: Install only with appropriately scoped tools and require explicit confirmation before irreversible or production-impacting actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/simoncatbot/react-loop) <br>
- [Detailed Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with structured thought, action, observation, and final answer sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only workflow; does not install code, request secrets, or add persistence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
