## Description: <br>
Runs SRSA daily review sessions, lets agents grade cards with again, hard, good, or easy, and prompts explicit memory add, delete, or update actions after review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cheanus](https://clawhub.ai/user/cheanus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run local spaced-repetition review sessions for agent memory, track due cards, and decide when remembered facts should be added, deleted, updated, overridden, or removed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review cards and local history may store sensitive personal data if users place it in prompts or answers. <br>
Mitigation: Avoid putting secrets or sensitive personal data into cards, and remove or override cards when stored material should not persist. <br>
Risk: Suggested memory add, delete, or update actions could make the agent's memory incorrect if applied without review. <br>
Mitigation: Review each proposed memory change before applying it, especially after again, hard, or good ratings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cheanus/srsa) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/cheanus) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local review state and a local SQLite database; review cards can contain user-provided memory material.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
