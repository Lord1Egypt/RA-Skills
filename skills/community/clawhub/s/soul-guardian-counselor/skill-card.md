## Description: <br>
Soul Guardian provides Chinese-language AI counseling support for emotional distress, family conflict, work stress, relationships, personal growth, and related life concerns while maintaining a local Markdown memory system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taohaowei](https://clawhub.ai/user/taohaowei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill for supportive counseling-style conversations, structured reflection, family-relationship guidance, emotional first aid, and continuity across sessions through local notes. It is intended as AI-assisted support, not as a substitute for licensed mental-health, medical, or emergency services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create and retain sensitive mental-health and family-relationship notes under ~/.counselor on the local machine, and the security review notes that this can occur without a clear opt-in at time of use. <br>
Mitigation: Use it only on private, unsynced devices; prefer explicit /counselor invocation; review or delete ~/.counselor regularly; and avoid storing real names, identifiers, or details you do not want retained. <br>
Risk: Counseling and crisis guidance from the skill is supportive AI output and is not a replacement for licensed professional care or emergency help. <br>
Mitigation: Treat crisis guidance as support only and contact qualified professionals or emergency services when safety, self-harm, abuse, or medical concerns are present. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/taohaowei/soul-guardian-counselor) <br>
- [Counselor Skill Definition](artifact/SKILL.md) <br>
- [Soul Guardian Design Philosophy](artifact/docs/design.md) <br>
- [Initialization Templates](artifact/references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Chinese conversational text with Markdown notes and local file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and update local Markdown records under ~/.counselor during use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
