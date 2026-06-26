## Description: <br>
Local Voice Input/Output for Agents using the AI Voice Agent API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ricardotrevisan](https://clawhub.ai/user/ricardotrevisan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to transcribe user-provided audio files and synthesize agent responses as audio through a separately running local Voice Agent API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends audio files and synthesis text to a separately operated local backend, so backend trust and data handling affect privacy. <br>
Mitigation: Install and use the skill only with a backend you trust, and avoid processing secrets, regulated data, or private messages unless that backend and AWS Polly handling are acceptable. <br>
Risk: The skill reads audio from user-supplied paths and writes synthesized audio to user-selected output paths. <br>
Mitigation: Use deliberate input files and safe output paths before running transcribe or synthesize commands. <br>


## Reference(s): <br>
- [Voice Agent on ClawHub](https://clawhub.ai/ricardotrevisan/voice-agent) <br>
- [Skill homepage](https://github.com/ricardotrevisan/ai-conversational-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Guidance] <br>
**Output Format:** [Plain text, generated audio files, and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a separately running backend API at http://localhost:8000; text-to-speech may be handled by AWS Polly through that backend.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
