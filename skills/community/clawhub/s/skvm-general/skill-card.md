## Description: <br>
Guides an agent through skvm CLI workflows for profiling models, AOT-compiling skills, running skill-assisted tasks, benchmarking, and managing compiled proposals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lec77](https://clawhub.ai/user/lec77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate skvm for model profiling, skill compilation, single-task runs, benchmarking, and proposal review. It is intended for agents helping users run or inspect skvm workflows without inventing unsupported CLI flags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to use sensitive model API credentials for LLM-calling skvm commands. <br>
Mitigation: Use a limited API key where possible and require the agent to stop and ask when the required key is unset. <br>
Risk: Profiling or benchmarking multiple models can incur meaningful API cost. <br>
Mitigation: Require explicit confirmation before multi-model profile or bench runs and quote the model count back to the user. <br>
Risk: Accepting skvm proposals can overwrite or deploy skill files. <br>
Mitigation: Only run proposal acceptance after the user explicitly asks to deploy, and otherwise limit proposal handling to list, show, reject, or cancel actions. <br>
Risk: The skvm installer is an external shell installer referenced by the skill. <br>
Mitigation: Tell users to review the installer themselves before running it; do not install skvm automatically. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lec77/skvm-general) <br>
- [SkillVM installer](https://skillvm.ai/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include prerequisite checks, command invocations, environment variable guidance, and user-confirmation prompts for costly or file-overwriting operations.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
