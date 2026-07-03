## Description: <br>
Getting started with Signet Mind - local mental health companion with grounding exercises, breathing guides, and mood tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amrree](https://clawhub.ai/user/amrree) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to set up Signet Mind, learn its local wellness tools, and understand privacy and safety expectations. It should not be used as a substitute for emergency services or professional mental-health care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mental-health conversations and mood data may be stored in readable local database files despite encryption claims. <br>
Mitigation: Review local data storage before use, restrict filesystem access, and avoid entering sensitive information unless the storage behavior is acceptable. <br>
Risk: Chat mode may pass recent history and profile context to a Signet CLI whose local-versus-remote behavior is unclear. <br>
Mitigation: Confirm the Signet CLI data flow before enabling chat mode and use offline-only configuration when privacy requirements demand it. <br>
Risk: The skill supports mental-health use cases but is not professional care or an emergency service. <br>
Mitigation: Keep crisis resources visible and direct users to emergency or professional support for urgent or clinical needs. <br>


## Reference(s): <br>
- [Signet Guide on ClawHub](https://clawhub.ai/amrree/skills/signet-guide) <br>
- [Find a Helpline](https://findahelpline.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wellness-tool instructions and privacy or safety cautions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
