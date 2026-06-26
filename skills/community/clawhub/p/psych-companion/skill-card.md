## Description: <br>
Psych Companion helps users structure emotion journals, identify mood and stress patterns, receive CBT- and mindfulness-based coping suggestions, and route crisis signals to professional support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and support agents use this skill for daily emotional check-ins, stress reflection, basic coping exercises, and escalation guidance when crisis language appears. It is general wellness support and not a substitute for clinical diagnosis, licensed counseling, or emergency services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mental-health support could be mistaken for diagnosis, treatment, or emergency response. <br>
Mitigation: Present outputs as general wellness guidance, keep disclaimers visible, and direct users to licensed professionals or emergency services for severe distress, self-harm, or suicide risk. <br>
Risk: Keyword-based crisis detection may miss urgent situations or trigger on ambiguous language. <br>
Mitigation: Treat crisis routing as a support prompt rather than a safety guarantee, and encourage immediate local emergency support whenever there may be imminent danger. <br>
Risk: Some hotline or emergency-resource examples may not match the user's country or local availability. <br>
Mitigation: Ask users to rely on current local emergency numbers and locally appropriate mental-health crisis services. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/harrylabsj/psych-companion) <br>
- [Emotion reference taxonomy](references/emotions.json) <br>
- [CBT and mindfulness techniques](references/cbt_techniques.json) <br>
- [Crisis keywords and referral text](references/crisis_keywords.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or structured text responses with emotion analysis, coping suggestions, and referral guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local reference JSON is used for emotion labels, CBT techniques, and crisis keyword matching; no persistence is indicated by the server evidence.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
