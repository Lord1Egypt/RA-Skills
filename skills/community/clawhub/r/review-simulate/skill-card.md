## Description: <br>
This skill runs Chinese voice interview practice sessions with ASR transcription, LLM-driven follow-up questions, TTS interviewer prompts, and structured feedback reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cows21](https://clawhub.ai/user/cows21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to conduct multi-round Chinese job interview practice for a target role, collect per-round scoring, and generate actionable improvement guidance. It supports voice-based practice through configured LLM, ASR, and TTS providers, with text input available when audio is not used. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends interview audio or text to configured external LLM, ASR, and TTS providers. <br>
Mitigation: Use dedicated API keys, confirm the configured providers are trusted, and use text input or --no-tts when reducing audio upload or generation is preferred. <br>
Risk: Practice answers and generated reports may contain sensitive employer, identity, or career information. <br>
Mitigation: Avoid sharing confidential details during practice and delete the outputs directory or custom report files when they contain sensitive interview content. <br>
Risk: Interview scores and feedback are practice guidance and should not be treated as real hiring decisions. <br>
Mitigation: Use the generated feedback as coaching input and review conclusions against the user's actual answers before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cows21/review-simulate) <br>
- [Prompt templates](references/prompts_cn.md) <br>
- [State schema](references/state_schema_cn.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, audio, guidance] <br>
**Output Format:** [Chinese interview prompts, per-round JSON evaluation records, optional generated audio, and a final structured report.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured LLM, ASR, and TTS API keys for full voice operation; reports and generated audio may be written to local outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
