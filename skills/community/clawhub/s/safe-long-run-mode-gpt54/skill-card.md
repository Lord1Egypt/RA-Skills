## Description: <br>
Operates long-running tasks safely when GPT-5.4 is the primary model by emphasizing segmented work, checkpoints, subagent delegation, and external-service throttling controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bwiley1989](https://clawhub.ai/user/bwiley1989) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent operators use this skill to manage long coding, research, documentation, build, Azure, and multi-agent tasks in a GPT-5.4-centered workflow. It helps keep work low-cost, resumable, and safer around external service limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checkpoint notes or delegated subagent prompts could expose credentials, private data, or sensitive work details. <br>
Mitigation: Define permitted checkpoint locations before starting, keep credentials and private data out of saved notes, and limit what each subagent receives. <br>
Risk: External services may throttle or reject long-running automated work. <br>
Mitigation: Batch requests, use backoff, avoid rapid polling, and require explicit approval before account-impacting, public, or external-service writes. <br>


## Reference(s): <br>
- [GPT-5.4 Only Long-Run Checklist](references/checklist.md) <br>
- [ClawHub skill page](https://clawhub.ai/bwiley1989/safe-long-run-mode-gpt54) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/bwiley1989) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with checklists and command recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce checkpoint notes, plans, task summaries, and resume points for long-running work.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
