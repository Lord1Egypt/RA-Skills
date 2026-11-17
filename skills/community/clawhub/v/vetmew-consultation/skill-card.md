## Description:

专业宠物（猫、狗及异宠）医疗问诊。基于 VetMew 3.0 API 提供症状分析与诊断建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zerojh](https://clawhub.ai/user/zerojh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to run multi-turn pet health consultations and pet-care Q&A for cats, dogs, and exotic pets through VetMew. It supports pet profiles, symptom text, optional medical images or image URLs for supported visual categories, and separate session handling for medical, exotic-pet, and Q&A conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pet health questions, pet profile details, and supplied images or image URLs are sent to VetMew.

Mitigation: Use the skill only when users accept that data flow; minimize unnecessary personal or sensitive details and avoid uploading images that are not needed for the consultation.

Risk: The VetMew token and conversation IDs can preserve access or session context beyond a single turn.

Mitigation: Keep VETMEW_AUTH_TOKEN scoped to VetMew, do not expose credentials in outputs, and clear stored conversation IDs when sessions are no longer needed or become invalid.

Risk: The dependency file lists unpinned Python packages, which can reduce reproducibility.

Mitigation: Install in a controlled environment and prefer a reviewed lockfile or pinned dependency versions before production deployment.

Risk: Generated pet medical guidance may be incomplete or inappropriate for urgent conditions.

Mitigation: Treat the output as informational support and direct urgent or severe cases to an in-person veterinary clinic.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zerojh/skills/vetmew-consultation)
- [VetMew Open Platform](https://open.vetmew.com/)
- [VetMew API service endpoint](https://platformx.vetmew.com)
- [VetMew pet breed catalog](https://oss-vetmew.vetmew.com/vetmew/pet_breed_ef8a9e.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Streaming CLI text with Markdown-style usage commands and conversation IDs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VETMEW_AUTH_TOKEN and can return CONVERSATION_ID values for multi-turn state.]

## Skill Version(s):

1.0.8 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
