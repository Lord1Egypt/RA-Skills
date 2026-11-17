## Description:

Turns an AI agent with persistent memory into a quit-smoking sponsor that provides evidence-based quit support protocols, safety boundaries, and a local timestamped logbook for adults quitting smoked tobacco.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metrox-eth](https://clawhub.ai/user/metrox-eth)

### License/Terms of Use:

MIT

## Use Case:

External adults who explicitly want quit-smoking support use this skill with an AI agent as a persistent sponsor for cravings, slips, relapse recovery, safety escalation, and long-term aftercare. It is designed to complement, not replace, medical care, crisis support, or professional treatment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive quit-smoking and health-related logbook data.

Mitigation: Keep the logbook local, let the person review or delete stored quit data, and avoid sharing quit details outside the quit-support context unless explicitly requested.

Risk: Users may mistake quit-smoking support for medical care or prescribing advice.

Mitigation: Present the skill as peer-style support only and refer medication questions, physical red flags, pregnancy, cardiac issues, psychiatric concerns, and dosing decisions to clinicians.

Risk: Acute distress or self-harm signals can appear during a quit attempt.

Mitigation: Pause the quit protocol, stay supportive, and direct the person to appropriate human crisis or emergency support.

Risk: The tobacco slip protocol could be unsafe if generalized to alcohol, opioids, or broader substance dependence.

Mitigation: Limit use to adult quit-smoking support and insist on professional care for alcohol dependence, opioid dependence, poly-substance dependence, or other out-of-scope conditions.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/metrox-eth/skills/quit-sponsor)
- [README](artifact/README.md)
- [Safety rails](artifact/SAFETY.md)
- [Model fit evaluation](artifact/MODEL_FIT.md)
- [Evidence references](artifact/references.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Conversational text with Markdown-compatible logbook entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local quit-support notes and recommendations; no external API calls or credential use are indicated by the release evidence.]

## Skill Version(s):

0.6.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
