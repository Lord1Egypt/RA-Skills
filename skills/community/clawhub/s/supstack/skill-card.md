## Description: <br>
Supplement Research helps an agent answer supplement questions using the SupStack evidence database, including safety, dosing, interactions, stack review, experiments, timing, and research alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DrBaher](https://clawhub.ai/user/DrBaher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to ask an OpenClaw agent for evidence-based supplement information, safety checks, stack optimization, self-experiment tracking, and new-study alerts. The skill is informational and does not diagnose, prescribe, or replace clinician guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retain sensitive supplement, medication, condition, allergy, preference, search, and experiment information in a local plain-text profile. <br>
Mitigation: Install and use it only when users understand what is stored, where the files live, how to delete them, and what health details they choose to share. <br>
Risk: Research alerts and experiment check-ins can create scheduled follow-up messages. <br>
Mitigation: Enable scheduled monitoring only with clear user consent, confirm the chosen frequency, and provide a direct way to stop monitoring. <br>
Risk: Supplement guidance can affect health decisions, especially for medications, pregnancy, medical conditions, or allergies. <br>
Mitigation: Keep responses informational, check interactions and contraindications before recommendations, and direct users to a healthcare professional for medical decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/DrBaher/supstack) <br>
- [Publisher Profile](https://clawhub.ai/user/DrBaher) <br>
- [SupStack Evidence Database](https://supstack.me) <br>
- [SupStack Public API](https://supstack.me/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with helper-script shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl and jq; may create local profile, monitor, and experiment files under the SupStack state directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
