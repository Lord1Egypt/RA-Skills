## Description: <br>
Runs lightweight self-audits of OpenClaw behavior, finds repeated failures, proposes safe config and process improvements, and tracks changes after incidents, silent-bot periods, rate-limit spikes, or weekly maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utromaya-code](https://clawhub.ai/user/utromaya-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators maintaining OpenClaw use this skill to audit reliability incidents, group repeated failures, propose minimal reversible fixes, and record weekly improvement outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic restarts, session cleanup, or configuration tuning could disrupt active OpenClaw service or make reliability worse if applied without review. <br>
Mitigation: Review proposed fixes before relying on them in production, keep a rollback path for configuration edits, and apply one reversible change per cycle. <br>
Risk: Audit reports may include sensitive information from logs or configuration context. <br>
Mitigation: Follow the skill guardrail to avoid exposing secrets in reports and require explicit approval for credential rotation, deletion, or other high-impact actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/utromaya-code/self-improver-lite-ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands, audit summaries, and action checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed low-risk maintenance actions, approval-gated changes, rollback notes, and weekly audit records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
