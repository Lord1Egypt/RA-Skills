## Description: <br>
Supermemory stores, recalls, and searches customer conversation insights through a memory layer for use across interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ipythoning](https://clawhub.ai/user/ipythoning) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and customer-facing agents use this skill to capture customer facts, preferences, market signals, and effective scripts, then recall relevant memories during later conversations. It is most useful where continuity across customer interactions improves follow-up quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retain sensitive customer, sales, or regulated data as memory records. <br>
Mitigation: Use a local-only configuration unless cloud storage is explicitly approved, avoid storing secrets, and confirm retention and deletion behavior before deployment. <br>
Risk: Automatic capture can store sensitive conversation details without sufficient user control. <br>
Mitigation: Disable auto-capture or gate it behind an explicit approval step for sensitive conversations. <br>


## Reference(s): <br>
- [Supermemory ClawHub release page](https://clawhub.ai/ipythoning/sdr-supermemory) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and CLI text or JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Memory records may persist until their TTL expires or they are explicitly deleted.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
