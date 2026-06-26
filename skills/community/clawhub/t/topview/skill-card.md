## Description: <br>
Topview lets an agent generate videos, images, talking avatars, and TTS audio through the Topview API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[topviewai](https://clawhub.ai/user/topviewai) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
External users, creators, marketers, and developers use this skill to have an agent create Topview videos, images, talking avatars, voice audio, and organized board results from natural-language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Topview credentials and stores them locally. <br>
Mitigation: Install only when comfortable linking a Topview account, and protect or remove the local credential file when access is no longer needed. <br>
Risk: Generation workflows may upload user media, voice samples, or other creative inputs to Topview or its storage providers. <br>
Mitigation: Use only media the user is allowed to upload, avoid sensitive or third-party biometric content without consent, and review inputs before submission. <br>
Risk: Tasks can spend Topview credits and some modules can delete boards or custom voices. <br>
Mitigation: Confirm credit-consuming tasks and destructive board or voice actions explicitly before running them. <br>
Risk: The security summary says network disclosures are not fully accurate. <br>
Mitigation: Review and accept Topview network access before installation, and use webhook URLs only when they are controlled by the user or organization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/topviewai/topview) <br>
- [Topview homepage](https://www.topview.ai) <br>
- [Authentication reference](artifact/references/auth.md) <br>
- [Video generation reference](artifact/references/video_gen.md) <br>
- [AI image reference](artifact/references/ai_image.md) <br>
- [Avatar reference](artifact/references/avatar4.md) <br>
- [Voice reference](artifact/references/voice.md) <br>
- [Board reference](artifact/references/board.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Media links] <br>
**Output Format:** [Markdown guidance with command invocations, generated media links, and board URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Topview account, local credentials, available credits, and selected user media or prompts for generation tasks.] <br>

## Skill Version(s): <br>
0.1.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
