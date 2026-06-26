## Description: <br>
Self-Improvement (LLM Memory) gives agents a local memory and reflection workflow for logging experience, extracting lessons, tracking preferences, proposing behavior updates, and checking whether changes helped. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucetangc](https://clawhub.ai/user/brucetangc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when they want an agent to maintain local long-term memory, capture feedback, summarize sessions, extract recurring patterns, and propose or apply updates to local guidance files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill keeps long-term local memory, including logs and preferences, which can retain sensitive or outdated information. <br>
Mitigation: Review the memory directory before enabling the skill, periodically inspect or delete stored logs and preferences, and use it only when persistent local memory is intended. <br>
Risk: Automatic learning cycles and promotions can change local guidance files and influence future agent behavior with too little user control. <br>
Mitigation: Avoid or disable automatic cycles where possible, review proposed promotions before relying on them, and verify changes before deployment. <br>
Risk: Backup ZIP import can restore untrusted memory data into the local workspace. <br>
Mitigation: Import only trusted backups, prefer non-overwrite imports, and inspect restored memory files before running learning or promotion commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/brucetangc/self-improvement-llm) <br>
- [Reflection Frameworks](references/reflection_frameworks.md) <br>
- [pskoett/self-improving-agent](https://clawhub.ai/pskoett/self-improving-agent) <br>
- [Hermes Agent](https://github.com/NousResearch/hermes-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local file-change proposals] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory logs, indexes, generated skill drafts, and guidance files when its scripts are run.] <br>

## Skill Version(s): <br>
2.2.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
