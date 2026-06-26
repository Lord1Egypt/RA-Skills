## Description: <br>
REFINE is an adaptive skill engine for structured session diagnostics, local error-pattern logging, feedback capture, session memory, and System Prompt Patch synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dttnpole-commits](https://clawhub.ai/user/dttnpole-commits) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use REFINE to capture short diagnostic labels and error patterns across sessions, store sanitized local memory, and generate local System Prompt Patch guidance from repeated failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores user-provided feedback, error messages, and context on local disk. <br>
Mitigation: Use only short, non-sensitive labels and metadata; avoid raw prompts, credentials, personal data, private customer logs, and full error text. <br>
Risk: Generated System Prompt Patch guidance could introduce incorrect or misleading instructions if applied without review. <br>
Mitigation: Review each generated patch before applying it to an agent's system prompt. <br>
Risk: Local diagnostic memory may retain information longer than intended. <br>
Mitigation: Periodically inspect or delete refine_memory.json according to the user's retention needs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dttnpole-commits/refine-agent) <br>
- [SkillPay upgrade page](https://skillpay.io/refine/upgrade) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Python return values and JSON-backed local memory, including patch_body text suitable for prepending to a system prompt] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [BASIC mode records sanitized local diagnostics; PRO mode can produce local failure analysis and System Prompt Patch text.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and changelog; artifact files also reference 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
